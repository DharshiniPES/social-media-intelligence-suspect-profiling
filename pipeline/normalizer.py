from core.evidence_model import EvidenceProfile
import re

def sanitize_username(username):
    """Clean usernames by stripping URLs and extra whitespace."""
    if not username:
        return ""
    # If it looks like a URL, extract the last path segment (the handle)
    if "http" in username:
        parts = username.strip("/").split("/")
        # Return the last part if it exists, otherwise empty
        return parts[-1] if parts else ""
    return username.strip()

def normalize_instagram(profile_data):
    evidence = EvidenceProfile()
    evidence.platform = "Instagram"
    
    # Use the sanitizer here
    evidence.username = sanitize_username(profile_data.get("username", ""))

    evidence.display_name = (profile_data.get("display_name") or profile_data.get("full_name") or "")
    evidence.bio = (profile_data.get("bio") or profile_data.get("biography") or "")
    evidence.profile_url = (profile_data.get("url") or profile_data.get("profile_url") or "")
    evidence.profile_image = (profile_data.get("profile_picture") or profile_data.get("avatar_url") or "")
    evidence.verified = profile_data.get("verified", False)
    evidence.followers = profile_data.get("followers", 0)
    evidence.following = profile_data.get("following", 0)
    evidence.posts_count = profile_data.get("posts_count", 0)

    posts = profile_data.get("posts") or profile_data.get("recent_posts") or []
    evidence.posts = posts

    for post in posts:
        caption = post.get("caption") or post.get("text") or ""
        evidence.captions.append(caption)
        evidence.hashtags.extend(re.findall(r"#(\w+)", caption))
        evidence.mentions.extend(re.findall(r"@(\w+)", caption))
        evidence.hyperlinks.extend(re.findall(r"https?://\S+", caption))
        timestamp = post.get("created_at") or post.get("timestamp") or ""
        if timestamp:
            evidence.timestamps.append(timestamp)

    evidence.emails.extend(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", evidence.bio))

    emoji_pattern = re.compile(
        "[" "\U0001F600-\U0001F64F" "\U0001F300-\U0001F5FF" "\U0001F680-\U0001F6FF" "\U0001F1E0-\U0001F1FF" "]+",
        flags=re.UNICODE
    )
    evidence.emojis = emoji_pattern.findall(evidence.bio + "\n" + "\n".join(evidence.captions))
    evidence.raw_data = profile_data
    return evidence

def normalize_github(profile_data):
    evidence = EvidenceProfile()
    evidence.platform = "GitHub"
    
    # Use the sanitizer here
    evidence.username = sanitize_username(profile_data.get("username", ""))
    
    evidence.display_name = profile_data.get("name", "")
    evidence.bio = profile_data.get("bio") or ""
    evidence.profile_url = profile_data.get("profile_url", "")
    evidence.profile_image = profile_data.get("avatar", "")
    evidence.followers = profile_data.get("followers", 0)
    evidence.following = profile_data.get("following", 0)
    evidence.posts_count = profile_data.get("public_repos", 0)

    repositories = profile_data.get("repositories", [])
    evidence.posts = repositories

    for repo in repositories:
        description = repo.get("description") or ""
        evidence.captions.append(description)
        if repo.get("language"): evidence.hashtags.append(repo["language"])
        if repo.get("topics"): evidence.hashtags.extend(repo["topics"])

    if profile_data.get("blog"): evidence.hyperlinks.append(profile_data["blog"])
    if profile_data.get("email"): evidence.emails.append(profile_data["email"])
    
    evidence.raw_data = profile_data
    return evidence

def normalize_website(profile_data):
    evidence = EvidenceProfile()
    evidence.platform = "Website"
    
    # Custom cleaning for domains
    domain = profile_data.get("domain", "")
    evidence.username = domain.replace("https://", "").replace("http://", "").strip("/")
    
    evidence.display_name = profile_data.get("title", "")
    evidence.bio = profile_data.get("description", "")
    evidence.profile_url = profile_data.get("url", "")
    evidence.hyperlinks.extend(profile_data.get("links", []))
    evidence.emails.extend(profile_data.get("emails", []))
    evidence.posts = []
    evidence.raw_data = profile_data
    return evidence