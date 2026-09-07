import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from evaluation.benchmark_runner import EvaluationRunner
from evaluation.report import build_summary_report


def main():
    runner = EvaluationRunner()

    conversation_records = [
        {
            "input_text": "Tell me something interesting about your weekend.",
            "conversation": [],
            "target_text": "",
        }
    ]

    conversation_result = runner.evaluate_conversation(
        conversation_records,
        lambda prompt, history: {
            "response": "What did you enjoy most about your weekend?"
        },
    )

    rag_result = runner.evaluate_rag(
        queries=["present perfect"],
        relevant_lists=[["grammar-present-perfect"]],
        retrieve_fn=lambda q: ["grammar-present-perfect", "past-simple"],
        k_values=(1, 3),
    )

    report = build_summary_report(
        {
            "conversation": conversation_result,
            "rag": rag_result,
        }
    )

    print(report)


if __name__ == "__main__":
    main()