from pathlib import Path

from ai.rag.text_splitter import StructureAwareTextSplitter


class KnowledgePreprocessor:
    def __init__(self, chunk_size=1200, overlap=150):
        self.splitter = StructureAwareTextSplitter(
            chunk_size=chunk_size,
            overlap=overlap
        )

    def _get_category(self, source):
        path = Path(source)

        try:
            return path.parent.name
        except Exception:
            return "unknown"

    def process_documents(self, documents):
        chunks = []

        for document in documents:
            text = document["text"].strip()
            metadata = document["metadata"].copy()

            if not text:
                continue

            metadata["category"] = self._get_category(
                metadata.get("source", "")
            )

            # Vocabulary TSV rows are already small structured records.
            # Do not split them again.
            if metadata.get("file_type") == "tsv":
                metadata["chunk_index"] = 0

                chunks.append({
                    "text": text,
                    "metadata": metadata
                })

                continue

            # PDFs and other long documents
            text_chunks = self.splitter.split_text(text)

            for chunk_index, chunk_text in enumerate(text_chunks):
                chunk_text = chunk_text.strip()

                if not chunk_text:
                    continue

                chunk_metadata = metadata.copy()
                chunk_metadata["chunk_index"] = chunk_index

                chunks.append({
                    "text": chunk_text,
                    "metadata": chunk_metadata
                })

        return chunks