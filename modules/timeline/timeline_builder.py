class TimelineBuilder:
    @staticmethod
    def build_timeline(profile):
        # Sorts the timestamps extracted in your normalizer
        return sorted(profile.timestamps)
    
    @staticmethod
    def get_posting_rhythm(profile):
        # Returns the average time difference between posts
        times = sorted(profile.timestamps)
        if len(times) < 2: return 0
        # Simple placeholder for rhythmic analysis
        return "Consistent"