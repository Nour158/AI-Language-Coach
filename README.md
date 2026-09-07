# AI Language Coach

## Assessment + Feedback

# Branch 2 ΓÇö Assessment + Feedback

Target branch: `feature/assessment-feedback`.

This implementation follows the AI Language Coach Branch-2 contract:

```python
evaluate_session(conversation_history) -> structured report JSON
```

It analyzes only learner/user messages and never scores assistant English.

## Required assessment files

Implemented exactly:

- `ai/assessment/grammar_analyzer.py`
- `ai/assessment/vocabulary_analyzer.py`
- `ai/assessment/fluency_analyzer.py`
- `ai/assessment/coherence_analyzer.py`
- `ai/assessment/mistake_tracker.py`
- `ai/assessment/proficiency_scorer.py`
- `ai/assessment/session_evaluator.py`

Also included: `sentence_structure_analyzer.py`, because Sentence Structure is a required assessment dimension, plus schemas/config/utils and an optional Qwen assessment layer.

## Required feedback files

Implemented exactly:

- `ai/feedback/correction_generator.py`
- `ai/feedback/explanation_generator.py`
- `ai/feedback/natural_rephraser.py`
- `ai/feedback/exercise_generator.py`
- `ai/feedback/feedback_pipeline.py`

Every important mistake supports:
`original`, `corrected`, `natural_alternative`, `category`, and `explanation`.

## Integration

Included:
- `backend/services/assessment_service.py`
- `evaluation/evaluate_assessment.py`

## CEFR / scoring rule

There is deliberately no numeric score-to-CEFR lookup table.

The report always labels current scoring as:

`experimental_heuristic_not_calibrated`

A CEFR value can only be returned as an explicitly marked experimental LLM hint when enough learner evidence exists. Otherwise it is `null`.

## Qwen integration

If Branch 1's `ai.llm.qwen_client.QwenClient` exists and is reachable, it is used for contextual assessment. If it is unavailable, Branch 2 falls back to deterministic analysis instead of crashing.

## Run tests

From the repo root:

```powershell
python -m pytest tests/test_branch2.py -q
```

## Git

```powershell
git checkout feature/assessment-feedback
git status
git add ai/assessment ai/feedback backend/services/assessment_service.py evaluation/evaluate_assessment.py tests/test_branch2.py BRANCH2_README.md
git commit -m "Complete session assessment and personalized feedback"
git push origin feature/assessment-feedback
```

Then open a PR from `feature/assessment-feedback` to `develop`.

---

## Data + Evaluation / Training Optimization

# Branch 3 ΓÇö Data + Evaluation

This branch provides the project-wide **data preparation and evaluation layer** for the AI Language Coach.

## Responsibilities covered

- Dataset discovery/loading
- Dataset normalization into one stable schema
- Deterministic train/validation/test splitting
- Conversation evaluation
- Grammar-correction evaluation
- Assessment evaluation
- RAG retrieval evaluation
- JSON evaluation reports
- Unit tests
- Command-line dataset preparation

## Datasets supported by the registry

The registry includes the datasets already selected for the project:

- ErAConD
- JFLEG
- TeacherStudentChatroomCorpus_v2
- Write & Improve Corpus 2024 v2

Because downloaded dataset layouts may differ, `load_records()` supports CSV, TSV, JSON, JSONL, and TXT files and can scan nested folders.

## Canonical data schema

Every normalized record has:

```python
{
    "id": "...",
    "dataset": "...",
    "task": "...",
    "input_text": "...",
    "target_text": "...",
    "conversation": [],
    "label": None,
    "metadata": {}
}
```

This prevents every model/evaluation script from needing dataset-specific code.

## Evaluation metrics

### Conversation
- Average response length
- Follow-up question rate
- Correction-overload rate
- Optional reference token F1

### RAG
- Hit Rate@K
- Recall@K
- Mean Reciprocal Rank (MRR)

### Assessment
- MAE
- RMSE
- Pearson correlation
- CEFR accuracy
- Error-type precision / recall / F1

### Grammar correction
- Exact match
- Token-level F1

These metrics are lightweight and do not require paid APIs.

## Prepare a dataset

From the repository root:

```powershell
python -m scripts.prepare_datasets `
  --dataset jfleg `
  --input data/datasets/jfleg `
  --output data/processed
```

Example for ErAConD:

```powershell
python -m scripts.prepare_datasets `
  --dataset eracond `
  --input data/datasets/eracond `
  --output data/processed
```

## Run smoke evaluation

```powershell
python -m scripts.run_branch3_smoke_eval
```

## Run tests

```powershell
python -m pytest tests/test_data_pipeline.py tests/test_common_metrics.py tests/test_rag_metrics.py tests/test_assessment_metrics.py tests/test_benchmark_runner.py -q
```

## Integration contracts

Branch 3 does not own the LLM, frontend, or assessment logic. It evaluates them through callbacks.

Conversation:

```python
runner.evaluate_conversation(records, generate_fn=generate_response)
```

Assessment:

```python
runner.evaluate_assessment(records, assess_fn=evaluate_session)
```

RAG:

```python
runner.evaluate_rag(queries, relevant_lists, retrieve_fn=retriever.retrieve)
```

This keeps Branch 3 independent while allowing it to test Branches 1 and 2.

## Recommended Git workflow

```powershell
git checkout feature/evaluation
```

Copy these into that branch:

```text
data_pipeline/
evaluation/
scripts/prepare_datasets.py
scripts/run_branch3_smoke_eval.py
tests/test_data_pipeline.py
tests/test_common_metrics.py
tests/test_rag_metrics.py
tests/test_assessment_metrics.py
tests/test_benchmark_runner.py
BRANCH3_README.md
```

Then:

```powershell
git status
git add data_pipeline evaluation scripts/prepare_datasets.py scripts/run_branch3_smoke_eval.py tests/test_data_pipeline.py tests/test_common_metrics.py tests/test_rag_metrics.py tests/test_assessment_metrics.py tests/test_benchmark_runner.py BRANCH3_README.md
git status
git commit -m "Implement data preparation and evaluation pipeline"
git push origin feature/evaluation
```

Avoid `git add .` if local datasets, caches, model files, or secrets are present.

## Important evaluation note

The current metric suite is a strong engineering baseline, not a claim that any one metric perfectly measures English ability. Final project conclusions should combine automatic metrics with a small manually reviewed validation set.
