import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from ai.config import LLM_MODEL_NAME


_tokenizer = None
_model = None


def get_device():
    """
    Return the best available device.
    """
    if torch.cuda.is_available():
        return "cuda"

    return "cpu"


def load_tokenizer():
    """
    Load the tokenizer once and reuse it.
    """
    global _tokenizer

    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(
            LLM_MODEL_NAME
        )

    return _tokenizer


def load_model():
    """
    Load the language model once and reuse it.
    """
    global _model

    if _model is None:
        print(f"Loading model: {LLM_MODEL_NAME}")

        _model = AutoModelForCausalLM.from_pretrained(
            LLM_MODEL_NAME,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto",
        )

        _model.eval()

    return _model