class AdversarialDetector:
    @staticmethod
    def calculate_bot_risk(profile):
        score = 0.0
        
        # Safely handle None values by defaulting them to 0
        posts = profile.posts_count if profile.posts_count is not None else 0
        followers = profile.followers if profile.followers is not None else 0
        
        # Check: High post count, low followers
        if posts > 1000 and followers < 10:
            score += 0.5
            
        # Check: Empty bio
        if not profile.bio or len(profile.bio) < 5:
            score += 0.3
            
        return min(score, 1.0)

    @staticmethod
    def is_adversarial(profile, threshold=0.5):
        return AdversarialDetector.calculate_bot_risk(profile) >= threshold