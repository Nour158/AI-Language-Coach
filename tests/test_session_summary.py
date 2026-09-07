from ai.llm.session_summary import SessionSummaryGenerator


generator = SessionSummaryGenerator()

history = [
    {
        "role": "user",
        "content": (
            "I want to improve my English because I plan "
            "to travel to London next year."
        ),
    },
    {
        "role": "assistant",
        "content": (
            "That's a great goal. What part of English "
            "would you like to improve most?"
        ),
    },
    {
        "role": "user",
        "content": (
            "Grammar is difficult for me, especially "
            "the present perfect tense."
        ),
    },
]

summary = generator.generate_summary(history)

print("\n===== SESSION SUMMARY =====")
print(summary)