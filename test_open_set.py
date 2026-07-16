from pipeline.search_pipeline import SearchPipeline
from pipeline.ranking_pipeline import RankingPipeline
from pipeline.normalizer import normalize_instagram
from modules.scrapers.instagram_collector import InstagramCollector
from modules.open_set.rejection import OpenSetRecognizer

target = normalize_instagram(
    InstagramCollector().scrape("instagram")
)

candidates = SearchPipeline.search(
    "instagram",
    ["Instagram", "GitHub"]
)

results = RankingPipeline.rank(
    target,
    candidates
)

decision = OpenSetRecognizer.evaluate(results)

print(decision)