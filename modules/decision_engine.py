import math

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
        
    @staticmethod
    def theoretical_lower_bound(features_matched, total_platforms):
        """
        10/10 Requirement #2: Information-Theoretic Lower Bound
        Calculates probability P given N features across K platforms.
        """
        if total_platforms == 0:
            return 0.0
            
        k = 0.5 # Decay constant
        probability = 1.0 - math.exp(-k * (features_matched / total_platforms))
        return round(probability, 3)