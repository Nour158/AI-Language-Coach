class CorrectionGenerator:
    def generate(self, mistakes):
        output = []
        for item in mistakes:
            copy = dict(item)
            if not str(copy.get("corrected", "")).strip():
                copy["corrected"] = copy.get("original", "")
            output.append(copy)
        return output
