class ConversationMemory:
    """
    Stores recent conversation messages and a session summary.
    """

    def __init__(self, max_messages=10):
        self.max_messages = max_messages
        self.messages = []
        self.summary = ""

    def add_message(self, role, content):
        self.messages.append({
            "role": role,
            "content": content,
        })

        # Keep only recent messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_recent_history(self):
        return self.messages

    def set_summary(self, summary):
        self.summary = summary

    def get_summary(self):
        return self.summary

    def clear(self):
        self.messages = []
        self.summary = ""