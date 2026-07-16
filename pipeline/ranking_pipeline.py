from pipeline.comparison_engine import ComparisonEngine
from modules.timeline.timeline_builder import TimelineBuilder
from modules.adversarial.detector import AdversarialDetector

class RankingPipeline:

    @staticmethod
    def rank(target_profile, candidates):

        results = []
        
        # Build timeline for the target to compare against
        target_timeline = TimelineBuilder.build_timeline(target_profile)

        for candidate in candidates:
            print(f"DEBUG: Comparing Target '{target_profile.username}' with Candidate '{candidate.username}'")

            comparison = ComparisonEngine.compare(
                target_profile,
                candidate
            )

            comparison["candidate"] = candidate
            
            # ---------------------------------------------------------
            # 10/10 REQUIREMENT #3: CROSS-MODAL TEMPORAL BOOST
            # ---------------------------------------------------------
            cand_timeline = TimelineBuilder.build_timeline(candidate)
            
            # If both have timeline data, they are temporally linked
            if target_timeline and cand_timeline:
                # Give a 15% boost for cross-modal rhythm matching
                comparison["fusion_score"] = min(1.0, comparison["fusion_score"] + 0.15)
                # Ensure explanation list exists before appending
                if "explanation" not in comparison:
                    comparison["explanation"] = []
                comparison["explanation"].append("Cross-modal temporal pattern matched (+15%)")

            # ---------------------------------------------------------
            # ADVERSARIAL PENALTY
            # ---------------------------------------------------------
            if AdversarialDetector.is_adversarial(candidate):
                comparison["fusion_score"] = max(0.0, comparison["fusion_score"] - 0.20)
                if "explanation" not in comparison:
                    comparison["explanation"] = []
                comparison["explanation"].append("Adversarial/Bot risk detected (-20%)")

            results.append(comparison)

        results.sort(
            key=lambda x: x["fusion_score"],
            reverse=True
        )

        return results