from typing import Dict


class ReliabilityEngine:
    """
    Computes evidence reliability for every forensic module.

    Reliability is NOT similarity.

    Reliability answers:

    'How trustworthy is this evidence?'
    """

    @staticmethod
    def compute(profile) -> Dict[str, float]:

        reliability = {}

        # ----------------------------------------
        # Username
        # Username almost always exists
        # ----------------------------------------

        reliability["username"] = (
            1.0 if profile.username else 0.0
        )

        # ----------------------------------------
        # Bio
        # Longer bios generally contain more evidence
        # ----------------------------------------

        bio_length = len(profile.bio.strip())

        if bio_length == 0:
            reliability["bio"] = 0.0

        elif bio_length < 25:
            reliability["bio"] = 0.30

        elif bio_length < 75:
            reliability["bio"] = 0.70

        else:
            reliability["bio"] = 1.0

        # ----------------------------------------
        # Stylometry
        # More words = better writing fingerprint
        # ----------------------------------------

        total_words = sum(
            len(caption.split())
            for caption in profile.captions
        )

        if total_words < 30:
            reliability["stylometry"] = 0.20

        elif total_words < 100:
            reliability["stylometry"] = 0.50

        elif total_words < 300:
            reliability["stylometry"] = 0.80

        else:
            reliability["stylometry"] = 1.0

        # ----------------------------------------
        # Behaviour
        # More posts = stronger behavioural fingerprint
        # ----------------------------------------

        post_count = len(profile.posts)

        if post_count < 3:
            reliability["behaviour"] = 0.25

        elif post_count < 10:
            reliability["behaviour"] = 0.60

        else:
            reliability["behaviour"] = 1.0

        # ----------------------------------------
        # Emoji
        # ----------------------------------------

        emoji_count = len(profile.emojis)

        if emoji_count == 0:
            reliability["emoji"] = 0.0

        elif emoji_count < 5:
            reliability["emoji"] = 0.40

        else:
            reliability["emoji"] = 1.0

        # ----------------------------------------
        # Temporal
        # ----------------------------------------

        timestamps = len(profile.timestamps)

        if timestamps < 3:
            reliability["temporal"] = 0.30

        elif timestamps < 10:
            reliability["temporal"] = 0.70

        else:
            reliability["temporal"] = 1.0

        # ----------------------------------------
        # Hyperlinks
        # ----------------------------------------

        links = len(profile.hyperlinks)

        if links == 0:
            reliability["hyperlink"] = 0.0

        elif links < 3:
            reliability["hyperlink"] = 0.50

        else:
            reliability["hyperlink"] = 1.0

        # ----------------------------------------
        # Hashtags
        # ----------------------------------------

        hashtags = len(profile.hashtags)

        if hashtags == 0:
            reliability["hashtag"] = 0.0

        elif hashtags < 5:
            reliability["hashtag"] = 0.50

        else:
            reliability["hashtag"] = 1.0

        return reliability