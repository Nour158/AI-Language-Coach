from data_pipeline.normalizer import normalize_dataset
from data_pipeline.splitter import split_records

def test_jfleg_normalization():
    rows = [{"sentence": "I has a car.", "correction": "I have a car."}]
    records = normalize_dataset(rows, "jfleg")
    assert records[0]["task"] == "grammar_correction"
    assert records[0]["input_text"] == "I has a car."
    assert records[0]["target_text"] == "I have a car."

def test_split_is_deterministic():
    records = [{"id": str(i)} for i in range(20)]
    a = split_records(records, seed=42)
    b = split_records(records, seed=42)
    assert [x["id"] for x in a["train"]] == [x["id"] for x in b["train"]]
    assert len(a["train"]) + len(a["validation"]) + len(a["test"]) == 20
