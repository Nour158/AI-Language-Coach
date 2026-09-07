from __future__ import annotations
import random
from typing import Dict, List

def split_records(records, train=0.8, validation=0.1, test=0.1, seed=42) -> Dict[str, List[dict]]:
    if round(train + validation + test, 8) != 1.0:
        raise ValueError("train + validation + test must equal 1.0")

    items = list(records)
    rng = random.Random(seed)
    rng.shuffle(items)

    n = len(items)
    train_end = int(n * train)
    val_end = train_end + int(n * validation)

    return {
        "train": items[:train_end],
        "validation": items[train_end:val_end],
        "test": items[val_end:],
    }
