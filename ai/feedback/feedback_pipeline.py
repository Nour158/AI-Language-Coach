from .correction_generator import CorrectionGenerator
from .explanation_generator import ExplanationGenerator
from .natural_rephraser import NaturalRephraser
from .exercise_generator import ExerciseGenerator

class FeedbackPipeline:
    def __init__(self):
        self.corrections = CorrectionGenerator()
        self.explanations = ExplanationGenerator()
        self.rephraser = NaturalRephraser()
        self.exercises = ExerciseGenerator()

    def process(self, mistakes, repeated_patterns, strengths, weaknesses):
        mistakes = self.corrections.generate(mistakes)
        mistakes = self.rephraser.generate(mistakes)
        mistakes = self.explanations.generate(mistakes)
        return {
            "mistakes": mistakes,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "exercises": self.exercises.generate(mistakes, repeated_patterns, weaknesses),
        }
