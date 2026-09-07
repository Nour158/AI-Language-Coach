from pydantic import BaseModel


class TranscriptionResponse(BaseModel):
    transcript: str
    language: str = "en"
    source: str = "whisper"
