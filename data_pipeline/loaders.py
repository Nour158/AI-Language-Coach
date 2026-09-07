from __future__ import annotations
import csv
import json
from pathlib import Path
from typing import Any, Dict, List

SUPPORTED = {".csv", ".tsv", ".json", ".jsonl", ".txt"}

def _load_json(path: Path) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return [x if isinstance(x, dict) else {"text": str(x)} for x in data]
    if isinstance(data, dict):
        for key in ("data", "records", "items", "examples"):
            if isinstance(data.get(key), list):
                return [x if isinstance(x, dict) else {"text": str(x)} for x in data[key]]
        return [data]
    return [{"text": str(data)}]

def _load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        rows.append(obj if isinstance(obj, dict) else {"text": str(obj)})
    return rows

def _load_delimited(path: Path, delimiter: str) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return [dict(row) for row in csv.DictReader(f, delimiter=delimiter)]

def _load_txt(path: Path) -> List[Dict[str, Any]]:
    return [{"text": line.strip()} for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

def load_file(path) -> List[Dict[str, Any]]:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".json":
        return _load_json(path)
    if suffix == ".jsonl":
        return _load_jsonl(path)
    if suffix == ".csv":
        return _load_delimited(path, ",")
    if suffix == ".tsv":
        return _load_delimited(path, "\t")
    if suffix == ".txt":
        return _load_txt(path)
    raise ValueError(f"Unsupported dataset file: {path}")

def load_records(path) -> List[Dict[str, Any]]:
    path = Path(path)
    if path.is_file():
        return load_file(path)

    records = []
    for file in sorted(path.rglob("*")):
        if file.is_file() and file.suffix.lower() in SUPPORTED and ".git" not in file.parts:
            for row in load_file(file):
                row = dict(row)
                row["_source_file"] = str(file)
                records.append(row)
    return records
