class ConditionalRetrieval:
    """
    Decides whether a message needs knowledge retrieval.
    """

    def should_retrieve(self, user_message):
        if not user_message:
            return False

        text = user_message.lower().strip()

        # Simple conversational messages normally
        # do not require retrieval.
        conversational_phrases = [
            "hello",
            "hi",
            "hey",
            "good morning",
            "good evening",
            "good night",
            "thank you",
            "thanks",
            "bye",
            "goodbye",
            "how are you",
        ]

        if text in conversational_phrases:
            return False

        # English-learning questions likely need RAG.
        learning_keywords = [
            "grammar",
            "tense",
            "vocabulary",
            "meaning",
            "difference",
            "correct",
            "incorrect",
            "explain",
            "example",
            "examples",
            "pronunciation",
            "phrase",
            "word",
            "sentence",
            "english",
            "use",
            "when should",
            "how do i say",
        ]

        return any(
            keyword in text
            for keyword in learning_keywords
        )