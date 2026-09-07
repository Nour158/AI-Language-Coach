from __future__ import annotations
from typing import Any, Dict

CANONICAL_FIELDS = {
    "id",
    "dataset",
    "task",
    "input_text",
    "target_text",
    "conversation",
    "label",
    "metadata",
}

def canonical_record(
    record_id: str,
    dataset: str,
    task: str,
    input_text: str = "",
    target_text: str = "",
    conversation=None,
    label=None,
    metadata=None,
) -> Dict[str, Any]:
    return {
        "id": str(record_id),
        "dataset": str(dataset),
        "task": str(task),
        "input_text": str(input_text or ""),
        "target_text": str(target_text or ""),
        "conversation": list(conversation or []),
        "label": label,
        "metadata": dict(metadata or {}),
    }

def validate_record(record: Dict[str, Any]) -> None:
    missing = CANONICAL_FIELDS - set(record)
    if missing:
        raise ValueError(f"Canonical record missing fields: {sorted(missing)}")
