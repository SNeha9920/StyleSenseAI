class ConcernService:

    THRESHOLDS = {
        "hydration": {
            "severe": 40,
            "moderate": 60,
            "mild": 75,
        },
        "texture": {
            "severe": 40,
            "moderate": 60,
            "mild": 75,
        },
        "brightness": {
            "severe": 40,
            "moderate": 60,
            "mild": 75,
        },
        "acne": {
            "severe": 40,
            "moderate": 60,
            "mild": 75,
        },
    }

    def detect_concerns(self, scores):
        concerns = []

        for metric, score in scores.items():

            if score is None:
                continue

            threshold = self.THRESHOLDS.get(metric)

            if not threshold:
                continue

            if score <= threshold["severe"]:
                severity = "severe"

            elif score <= threshold["moderate"]:
                severity = "moderate"

            elif score <= threshold["mild"]:
                severity = "mild"

            else:
                continue

            concerns.append({
                "metric": metric,
                "score": score,
                "severity": severity,
            })

        return concerns