from fastapi import APIRouter

from backend.schemas.session import (
    SessionEvaluationRequest,
    SessionEvaluationResponse,
)
from backend.services.assessment_service import evaluate_session

router = APIRouter(prefix="/session", tags=["Session"])


@router.post("/evaluate", response_model=SessionEvaluationResponse)
def evaluate(request: SessionEvaluationRequest):
    return evaluate_session(request.history)
