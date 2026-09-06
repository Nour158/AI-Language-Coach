from pathlib import Path
from ai.speech.whisper_stt import transcribe_audio


def transcribe_uploaded_audio(file_path: Path) -> dict:
    return transcribe_audio(file_path)
