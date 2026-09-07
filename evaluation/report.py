from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone

def build_summary_report(results, metadata=None):
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "metadata": dict(metadata or {}),
        "results": dict(results or {}),
    }

def save_report(report, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return path
