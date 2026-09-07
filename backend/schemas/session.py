from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from backend.schemas.chat import Message


class Mistake(BaseModel):
    original: str
    corrected: str
    natural_alternative: Optional[str] = None
    category: str
    explanation: str


class SessionEvaluationRequest(BaseModel):
    history: List[Message]


class SessionEvaluationResponse(BaseModel):
    overall_score: float
    cefr_level: Optional[str] = None
    scores: Dict[str, float]
    strengths: List[str]
    weaknesses: List[str]
    mistakes: List[Mistake]
    repeated_patterns: List[str]
    exercises: List[str]
    source: str = "mock"
