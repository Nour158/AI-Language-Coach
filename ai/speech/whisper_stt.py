from pathlib import Path

from ai.speech.audio_utils import validate_audio_file


def transcribe_audio(file_path: Path) -> dict:
    """
    Whisper Speech-to-Text.

    This module ONLY converts speech to text.
    It must not assess grammar, fluency, proficiency, or CEFR level.

    Recommended package for local use:
        pip install faster-whisper

    For now, if faster-whisper is not installed, this returns a clear demo
    transcript instead of crashing the entire application.
    """
    validate_audio_file(file_path)

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return {
            "transcript": "[Demo STT] Audio received successfully. Install faster-whisper for real transcription.",
            "language": "en",
            "source": "demo",
        }

    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8",
    )

    segments, info = model.transcribe(str(file_path))
    transcript = " ".join(segment.text.strip() for segment in segments).strip()

    return {
        "transcript": transcript,
        "language": info.language or "en",
        "source": "whisper",
    }
