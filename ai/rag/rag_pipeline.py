from ai.rag.conditional_retrieval import ConditionalRetrieval
from ai.rag.query_rewriter import QueryRewriter
from ai.rag.retriever import HybridRetriever
from ai.rag.reranker import Reranker
from ai.prompts.conversation_prompts import ConversationPromptBuilder
from ai.llm.qwen_client import QwenClient


class RAGPipeline:
    """
    Full conversational RAG pipeline for the AI Language Coach.

    Flow:
        User message
            ↓
        Conditional retrieval
            ↓
        History-aware query rewriting using Qwen
            ↓
        Hybrid retrieval
            ↓
        RRF
            ↓
        Reranker
            ↓
        Final Top-K context
            ↓
        Conversation prompt builder
            ↓
        Qwen generation
            ↓
        Structured JSON-friendly result
    """

    def __init__(
        self,
        collection_name="language_coach",
        retrieval_top_k=10,
        final_top_k=5,
    ):
        print("Initializing RAG pipeline...")

        self.conditional_retrieval = ConditionalRetrieval()
        self.query_rewriter = QueryRewriter()

        self.retriever = HybridRetriever(
            collection_name=collection_name,
            initial_top_k=retrieval_top_k,
            final_top_k=retrieval_top_k,
        )

        self.reranker = Reranker(
            top_k=final_top_k
        )

        self.prompt_builder = ConversationPromptBuilder()
        self.qwen = QwenClient()

        print("RAG pipeline ready.")

    def process(
        self,
        user_message,
        conversation_history=None,
        session_summary="",
    ):
        """
        Process a user message through the complete conversational
        RAG pipeline and generate the final answer using Qwen.

        Returns:
            dict: JSON-friendly structured response.
        """

        if not user_message or not user_message.strip():
            raise ValueError("user_message cannot be empty.")

        conversation_history = conversation_history or []

        # --------------------------------------------------
        # 1. Decide whether RAG is needed
        # --------------------------------------------------

        needs_rag = self.conditional_retrieval.should_retrieve(
            user_message
        )

        retrieved_context = []
        retrieval_query = user_message
        rewrite_prompt = None

        # --------------------------------------------------
        # 2. Query rewriting + retrieval
        # --------------------------------------------------

        if needs_rag:

            # Rewrite vague follow-up questions using history.
            #
            # Example:
            # "When should I use it?"
            #
            # becomes:
            # "When should I use the present perfect tense?"
            if conversation_history:

                rewrite_prompt = (
                    self.query_rewriter.build_rewrite_prompt(
                        user_message=user_message,
                        conversation_history=conversation_history,
                    )
                )

                try:
                    rewritten_query = self.qwen.generate(
                        rewrite_prompt,
                        max_new_tokens=64,
                    )

                    if rewritten_query and rewritten_query.strip():
                        retrieval_query = rewritten_query.strip()

                except Exception as exc:
                    print(
                        "Warning: query rewriting failed. "
                        "Using original user message."
                    )
                    print(exc)

            # ----------------------------------------------
            # Hybrid dense + sparse retrieval
            # ----------------------------------------------

            hybrid_results = self.retriever.retrieve(
                retrieval_query
            )

            # ----------------------------------------------
            # Cross-encoder reranking
            # ----------------------------------------------

            retrieved_context = self.reranker.rerank(
                retrieval_query,
                hybrid_results,
            )

        # --------------------------------------------------
        # 3. Build final conversation prompt
        # --------------------------------------------------

        final_prompt = self.prompt_builder.build_prompt(
            user_message=user_message,
            conversation_history=conversation_history,
            session_summary=session_summary,
            retrieved_context=retrieved_context,
        )

        # --------------------------------------------------
        # 4. Generate final response using Qwen
        # --------------------------------------------------

        response_text = self.qwen.generate(
            final_prompt,
            max_new_tokens=256,
        )

        # --------------------------------------------------
        # 5. Prepare clean source metadata
        # --------------------------------------------------

        sources = []
        seen_sources = set()

        for result in retrieved_context:

            metadata = result.get("metadata", {})

            source = metadata.get("source")
            category = metadata.get("category")
            page = metadata.get("page")

            source_key = (
                source,
                category,
                page,
            )

            # Avoid duplicate source/page entries.
            if source_key not in seen_sources:

                seen_sources.add(source_key)

                sources.append(
                    {
                        "source": source,
                        "category": category,
                        "page": page,
                    }
                )

        # --------------------------------------------------
        # 6. Return structured JSON-friendly result
        # --------------------------------------------------

        return {
            "response": response_text,
            "user_message": user_message,
            "needs_rag": needs_rag,
            "retrieval_query": retrieval_query,
            "sources": sources,
            "metadata": {
                "model": "Qwen/Qwen2.5-7B-Instruct",
                "retrieved_chunks": len(retrieved_context),
                "unique_sources": len(sources),
            },
        }

    def close(self):
        """
        Close Qdrant resources.
        """

        self.retriever.close()