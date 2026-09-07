from pathlib import Path

# =========================================================
# Project Paths
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
VECTOR_DB_DIR = DATA_DIR / "qdrant"


# =========================================================
# LLM Configuration
# =========================================================

# Final / target model for the graduation project
TARGET_LLM_MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"

# Smaller model used locally during development
LLM_MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

MAX_NEW_TOKENS = 256
TEMPERATURE = 0.7
TOP_P = 0.9


# =========================================================
# Embedding Configuration
# =========================================================

EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5"


# =========================================================
# Retrieval Configuration
# =========================================================

TOP_K = 5
RERANK_TOP_K = 3


# =========================================================
# Conversation Memory
# =========================================================

MAX_HISTORY_MESSAGES = 10