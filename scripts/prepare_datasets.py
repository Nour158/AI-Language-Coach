from __future__ import annotations
import argparse
from pathlib import Path

from data_pipeline.loaders import load_records
from data_pipeline.normalizer import normalize_dataset
from data_pipeline.splitter import split_records
from data_pipeline.io import write_jsonl

def main():
    parser = argparse.ArgumentParser(description="Normalize and split AI Language Coach datasets.")
    parser.add_argument("--dataset", required=True, help="Dataset registry name.")
    parser.add_argument("--input", required=True, help="Dataset file or folder.")
    parser.add_argument("--output", default="data/processed", help="Output directory.")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    raw = load_records(args.input)
    normalized = normalize_dataset(raw, args.dataset)
    splits = split_records(normalized, seed=args.seed)

    out_dir = Path(args.output) / args.dataset
    for split_name, records in splits.items():
        write_jsonl(records, out_dir / f"{split_name}.jsonl")

    print(f"Loaded raw records: {len(raw)}")
    print(f"Normalized records: {len(normalized)}")
    for split_name, records in splits.items():
        print(f"{split_name}: {len(records)}")
    print(f"Saved to: {out_dir}")

if __name__ == "__main__":
    main()
