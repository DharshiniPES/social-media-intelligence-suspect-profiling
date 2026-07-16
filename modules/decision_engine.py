class DecisionEngine:

    @staticmethod
    def classify(score):

        if score >= 0.90:
            return "VERY HIGH"

        elif score >= 0.75:
            return "HIGH"

        elif score >= 0.60:
            return "MEDIUM"

        elif score >= 0.40:
            return "LOW"

        return "VERY LOW"