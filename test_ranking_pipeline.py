from pipeline.search_pipeline import SearchPipeline
from pipeline.ranking_pipeline import RankingPipeline
from pipeline.normalizer import normalize_instagram
from modules.scrapers.instagram_collector import InstagramCollector

# Build target profile
target_raw = InstagramCollector().scrape("instagram")
target = normalize_instagram(target_raw)

# Collect candidates
candidates = SearchPipeline.search(
    "instagram",
    ["Instagram", "GitHub"]
)

# Rank
results = RankingPipeline.rank(
    target,
    candidates
)

print("\nTOP MATCHES\n")

for r in results:

    print("=" * 60)

    print("Platform :", r["candidate"].platform)

    print("Username :", r["candidate"].username)

    print("Fusion   :", r["fusion_score"])

    print("Reason   :", r["explanation"])