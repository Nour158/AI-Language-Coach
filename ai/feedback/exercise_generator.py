from ai.assessment.config import MAX_EXERCISES

TEMPLATES = {
    "subject_verb_agreement": {
        "type": "multiple_choice",
        "skill": "subject_verb_agreement",
        "question": "Choose: A) She go every day. B) She goes every day.",
        "answer": "B",
        "why": "Practices subject-verb agreement.",
    },
    "verb_form": {
        "type": "fill_in_the_blank",
        "skill": "verb_form",
        "question": "I have _____ there before. (go)",
        "answer": "gone",
        "why": "Practices the past participle after have/has.",
    },
    "comparative": {
        "type": "correction",
        "skill": "comparatives",
        "question": "Correct: This is more easier.",
        "answer": "This is easier.",
        "why": "Practices avoiding double comparatives.",
    },
    "sentence_structure": {
        "type": "combine_sentences",
        "skill": "sentence_structure",
        "question": "Combine: I was tired. I finished my work.",
        "answer": "Although I was tired, I finished my work.",
        "why": "Practices clause linking.",
    },
}

class ExerciseGenerator:
    def generate(self, mistakes, repeated_patterns, weaknesses):
        categories = [p.get("category") for p in repeated_patterns]
        categories += [m.get("category") for m in mistakes]
        output, used = [], set()

        for category in categories:
            if category in TEMPLATES and category not in used:
                exercise = dict(TEMPLATES[category])
                exercise["based_on_observed_weakness"] = category
                output.append(exercise)
                used.add(category)
            if len(output) >= MAX_EXERCISES:
                return output

        if weaknesses and len(output) < MAX_EXERCISES:
            output.append({
                "type": "guided_production",
                "skill": "personalized_review",
                "question": "Write 4-5 sentences using one linking word and one two-clause sentence.",
                "answer": "Open-ended.",
                "why": "Targets weaknesses identified in this session.",
                "based_on_observed_weakness": weaknesses[0],
            })
        return output[:MAX_EXERCISES]
