from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from backend.schemas.chat import Message


class ConversationSession(BaseModel):
    session_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    started_at: datetime = Field(
        default_factory=datetime.now
    )

    ended_at: Optional[datetime] = None

    messages: List[Message] = []

    status: str = "active"