from ai.llm.generation import ConversationGenerator


generator = ConversationGenerator()

messages = [
    {
        "role": "system",
        "content": (
            "You are a friendly English conversation partner. "
            "Keep the conversation natural and do not correct every mistake."
        )
    },
    {
        "role": "user",
        "content": "Hi! I want to practice English. I like travelling."
    }
]

response = generator.generate_response(messages)

print("\nAssistant:")
print(response)