from __future__ import annotations
from typing import Any, Dict, Iterable, List, Sequence
from .dataset_registry import DatasetRegistry
from .schemas import canonical_record

def _pick(row: Dict[str, Any], candidates: Sequence[str], default=""):
    lowered = {str(k).lower(): k for k in row.keys()}
    for name in candidates:
        key = lowered.get(name.lower())
        if key is not None and row.get(key) not in (None, ""):
            return row.get(key)
    return default

def _conversation_from_row(row: Dict[str, Any]):
    if isinstance(row.get("conversation"), list):
        return row["conversation"]
    if isinstance(row.get("messages"), list):
        return row["messages"]

    text = _pick(row, ("text", "utterance", "message", "content"), "")
    role = _pick(row, ("role", "speaker"), "")
    if text:
        return [{"role": str(role or "user"), "content": str(text)}]
    return []

def normalize_dataset(
    records: Iterable[Dict[str, Any]],
    dataset_name: str,
    registry: DatasetRegistry | None = None,
) -> List[Dict[str, Any]]:
    registry = registry or DatasetRegistry()
    spec = registry.get(dataset_name)
    if spec is None:
        raise ValueError(f"Unknown dataset: {dataset_name}")

    out = []
    for index, row in enumerate(records):
        row = dict(row)
        input_text = _pick(
            row,
            spec.preferred_input_fields + ("text", "input", "source", "prompt", "utterance", "essay", "response"),
            "",
        )
        target_text = _pick(
            row,
            spec.preferred_target_fields + ("target", "reference", "correction", "corrected"),
            "",
        )
        label = _pick(
            row,
            spec.preferred_label_fields + ("label", "cefr", "level", "score"),
            None,
        )

        conversation = _conversation_from_row(row) if spec.task == "conversation" else []
        record_id = _pick(row, ("id", "example_id", "uid"), f"{spec.name}-{index}")

        metadata = {
            k: v for k, v in row.items()
            if k not in {
                "text","input","source","prompt","utterance","essay","response",
                "target","reference","correction","corrected","label","cefr","level","score",
                "conversation","messages"
            }
        }

        out.append(
            canonical_record(
                record_id=record_id,
                dataset=spec.name,
                task=spec.task,
                input_text=input_text,
                target_text=target_text,
                conversation=conversation,
                label=label,
                metadata=metadata,
            )
        )
    return out
