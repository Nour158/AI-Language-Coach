# Branch 2 — Assessment + Feedback

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
