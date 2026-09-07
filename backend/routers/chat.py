from fastapi import APIRouter

from backend.schemas.chat import (
    ChatRequest,
    ChatResponse,
    Message,
)

from backend.services.conversation_service import (
    generate_assistant_response,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):

    assistant_text = generate_assistant_response(
        user_message=request.message,
        conversation_history=request.history,
    )

    updated_history = list(request.history)

    user_metadata = {
        "input_type": request.input_type
    }

    if request.input_type == "voice":
        user_metadata["transcript"] = request.message

    updated_history.append(
        Message(
            role="user",
            content=request.message,
            metadata=user_metadata,
        )
    )

    updated_history.append(
        Message(
            role="assistant",
            content=assistant_text,
            metadata={
                "source": "conversation_service"
            },
        )
    )

    return ChatResponse(
        response=assistant_text,
        history=updated_history,
        source="mock",
    )