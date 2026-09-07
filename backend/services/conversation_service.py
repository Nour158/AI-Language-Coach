from typing import List

from backend.schemas.chat import Message


def generate_assistant_response(user_message: str, conversation_history: List[Message]) -> str:
    """
    Temporary Role 1 integration point.

    Replace this mock implementation later with the real Branch 1 function:
        generate_response(user_message, conversation_history)

    The API route does not need to change when the real model is integrated.
    """
    text = user_message.strip()

    if not text:
        return "Please write something so we can continue the conversation."

    return (
        f"That's interesting. You said: \"{text}\" "
        "Can you tell me a little more about that?"
    )
