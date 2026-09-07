from ai.llm.base_model import BaseLanguageModel


class ConversationGenerator:
    """
    High-level interface for conversation generation.
    """

    def __init__(self):
        self.llm = BaseLanguageModel()

    def generate_response(self, messages):
        """
        Generate one assistant response.
        """
        return self.llm.generate(messages)