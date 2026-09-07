from pathlib import Path

import pytest

from ai.speech.audio_utils import validate_audio_file


def test_missing_audio_file_raises_error():
    with pytest.raises(FileNotFoundError):
        validate_audio_file(Path("missing_audio_file.wav"))
