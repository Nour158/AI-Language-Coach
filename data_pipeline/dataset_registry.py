from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass(frozen=True)
class DatasetSpec:
    name: str
    task: str
    description: str
    license_note: str = ""
    preferred_input_fields: tuple = ()
    preferred_target_fields: tuple = ()
    preferred_label_fields: tuple = ()

DATASET_REGISTRY: Dict[str, DatasetSpec] = {
    "eracond": DatasetSpec(
        name="eracond",
        task="conversation",
        description="Conversation-oriented learner data used for dialogue/evaluation experiments.",
        preferred_input_fields=("text", "utterance", "input", "prompt"),
    ),
    "jfleg": DatasetSpec(
        name="jfleg",
        task="grammar_correction",
        description="Grammar correction benchmark with learner sentences and corrected references.",
        preferred_input_fields=("sentence", "input", "source", "original"),
        preferred_target_fields=("correction", "target", "reference", "corrected"),
    ),
    "teacherstudentchatroomcorpus_v2": DatasetSpec(
        name="TeacherStudentChatroomCorpus_v2",
        task="conversation",
        description="Teacher-student dialogue data for conversational behavior analysis.",
        preferred_input_fields=("text", "utterance", "message"),
    ),
    "write-and-improve-corpus-2024-v2": DatasetSpec(
        name="write-and-improve-corpus-2024-v2",
        task="assessment",
        description="Learner writing corpus suitable for proficiency and feedback evaluation.",
        preferred_input_fields=("text", "essay", "response", "writing"),
        preferred_label_fields=("cefr", "level", "score", "label"),
    ),
}

class DatasetRegistry:
    def __init__(self, registry=None):
        self.registry = dict(registry or DATASET_REGISTRY)

    def get(self, name: str) -> Optional[DatasetSpec]:
        key = name.lower()
        for dataset_name, spec in self.registry.items():
            if dataset_name.lower() == key or spec.name.lower() == key:
                return spec
        return None

    def names(self):
        return list(self.registry)
