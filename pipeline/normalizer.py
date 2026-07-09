from core.evidence_model import EvidenceProfile
import re


def normalize_instagram(profile_data):
    """
    Normalize Instagram intelligence output into a universal EvidenceProfile.
    Supports both raw CreatorCrawl output and InstagramIntelligence output.
    """

    evidence = EvidenceProfile()

    # -------------------------------------------------
    # Identity
    # -------------------------------------------------

    evidence.platform = "Instagram"

    evidence.username = profile_data.get("username", "")

    evidence.display_name = (
        profile_data.get("display_name")
        or profile_data.get("full_name")
        or ""
    )

    evidence.bio = (
        profile_data.get("bio")
        or profile_data.get("biography")
        or ""
    )

    evidence.profile_url = (
        profile_data.get("url")
        or profile_data.get("profile_url")
        or ""
    )

    evidence.profile_image = (
        profile_data.get("profile_picture")
        or profile_data.get("avatar_url")
        or ""
    )

    evidence.verified = profile_data.get("verified", False)

    # -------------------------------------------------
    # Network
    # -------------------------------------------------

    evidence.followers = profile_data.get("followers", 0)
    evidence.following = profile_data.get("following", 0)
    evidence.posts_count = profile_data.get("posts_count", 0)

    # -------------------------------------------------
    # Posts
    # -------------------------------------------------

    posts = (
        profile_data.get("posts")
        or profile_data.get("recent_posts")
        or []
    )

    evidence.posts = posts

    for post in posts:

        caption = (
            post.get("caption")
            or post.get("text")
            or ""
        )

        evidence.captions.append(caption)

        # -----------------------------
        # Hashtags
        # -----------------------------

        evidence.hashtags.extend(
            re.findall(r"#(\w+)", caption)
        )

        # -----------------------------
        # Mentions
        # -----------------------------

        evidence.mentions.extend(
            re.findall(r"@(\w+)", caption)
        )

        # -----------------------------
        # Hyperlinks
        # -----------------------------

        evidence.hyperlinks.extend(
            re.findall(r"https?://\S+", caption)
        )

        # -----------------------------
        # Timestamp
        # -----------------------------

        timestamp = (
            post.get("created_at")
            or post.get("timestamp")
            or ""
        )

        if timestamp:
            evidence.timestamps.append(timestamp)

    # -------------------------------------------------
    # Emails
    # -------------------------------------------------

    evidence.emails.extend(

        re.findall(

            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",

            evidence.bio

        )

    )

    # -------------------------------------------------
    # Emojis
    # -------------------------------------------------

    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "]+",
        flags=re.UNICODE
    )

    evidence.emojis = emoji_pattern.findall(
        evidence.bio + "\n" + "\n".join(evidence.captions)
    )

    # -------------------------------------------------
    # Raw Response
    # -------------------------------------------------

    evidence.raw_data = profile_data

    return evidence