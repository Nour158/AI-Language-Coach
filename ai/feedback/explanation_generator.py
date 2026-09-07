DEFAULTS = {
    "subject_verb_agreement": "Make the verb agree with the subject.",
    "verb_form": "Check the verb form required by the auxiliary or tense.",
    "comparative": "Use one comparative form rather than combining two.",
    "sentence_structure": "Connect clauses clearly and avoid fragments.",
}

class ExplanationGenerator:
    def generate(self, mistakes):
        output = []
        for item in mistakes:
            copy = dict(item)
            if not str(copy.get("explanation", "")).strip():
                copy["explanation"] = DEFAULTS.get(
                    copy.get("category"),
                    "Review this pattern and compare it with the corrected version."
                )
            output.append(copy)
        return output
