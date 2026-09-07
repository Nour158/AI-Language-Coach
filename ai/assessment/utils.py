import re

WORD_RE = re.compile(r"\b[A-Za-z]+(?:'[A-Za-z]+)?\b")
LEARNER_ROLES = {"user", "learner", "student"}

def learner_messages(history):
    result = []
    for item in history or []:
        if not isinstance(item, dict):
            continue
        role = str(item.get("role", "")).lower().strip()
        content = str(item.get("content", "")).strip()
        if role in LEARNER_ROLES and content:
            result.append(item)
    return result

def join_text(messages):
    return "\n".join(str(m.get("content", "")).strip() for m in messages if m.get("content"))

def tokenize(text):
    return [m.group(0).lower() for m in WORD_RE.finditer(text or "")]

def sentence_split(text):
    text = " ".join((text or "").split())
    if not text:
        return []
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

def optional_metadata(messages):
    return [m["metadata"] for m in messages if isinstance(m.get("metadata"), dict)]
