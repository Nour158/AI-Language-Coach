from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str = Field(min_length=1)

    metadata: Optional[Dict[str, Any]] = None


class ChatRequest(BaseModel):
    session_id: str
    message: str = Field(min_length=1)

    history: List[Message] = []

    input_type: Literal["text", "voice"] = "text"


class ChatResponse(BaseModel):
    response: str

    history: List[Message]

    source: str = "mock"