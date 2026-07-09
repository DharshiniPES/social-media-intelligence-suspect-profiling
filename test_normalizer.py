from pipeline.normalizer import normalize_instagram

# Simulate a CreatorCrawl response
sample_data = {
    "username": "testuser",
    "full_name": "Test User",
    "biography": "Cybersecurity enthusiast 👨‍💻 Contact: test@example.com",
    "profile_url": "https://instagram.com/testuser",
    "avatar_url": "https://example.com/avatar.jpg",
    "verified": True,
    "followers": 1200,
    "following": 300,
    "posts_count": 2,
    "recent_posts": [
        {
            "caption": "Learning #Python with @openai https://example.com",
            "created_at": "2026-07-09T10:00:00"
        },
        {
            "caption": "Another day, another #CyberSecurity post 🔒",
            "created_at": "2026-07-08T15:30:00"
        }
    ]
}

evidence = normalize_instagram(sample_data)

print(evidence)
print("Username:", evidence.username)
print("Bio:", evidence.bio)
print("Captions:", evidence.captions)
print("Hashtags:", evidence.hashtags)
print("Mentions:", evidence.mentions)
print("Hyperlinks:", evidence.hyperlinks)
print("Emails:", evidence.emails)
print("Timestamps:", evidence.timestamps)