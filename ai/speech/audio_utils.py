from pathlib import Path


def validate_audio_file(file_path: Path) -> None:
    if not file_path.exists():
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    if file_path.stat().st_size == 0:
        raise ValueError("Audio file is empty.")
