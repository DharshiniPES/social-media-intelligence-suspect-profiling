from pipeline.search_pipeline import SearchPipeline

profiles = SearchPipeline.search(
    "instagram",
    ["Instagram", "GitHub"]
)

print()

print("=" * 50)

for profile in profiles:

    print(profile.platform)

    print(profile.username)

    print(profile.bio[:100])

    print("-" * 50)