class NaturalRephraser:
    def generate(self, mistakes):
        output = []
        for item in mistakes:
            copy = dict(item)
            if not str(copy.get("natural_alternative", "")).strip():
                copy["natural_alternative"] = copy.get("corrected") or copy.get("original", "")
            output.append(copy)
        return output
