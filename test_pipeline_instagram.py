from modules.scrapers.instagram_scraper import InstagramScraper
from dashboard.instagram_intelligence import InstagramIntelligence
from pipeline.intelligence_pipeline import IntelligencePipeline

scraper = InstagramScraper()

profile = scraper.scrape("instagram")

intel = InstagramIntelligence().analyze(profile)

pipeline = IntelligencePipeline()

normalized = pipeline.normalize_instagram(intel)

evidence = pipeline.run(normalized)

print("\n========== PIPELINE ==========\n")

print("Source:", evidence["source"])
print("Username:", evidence["identity"]["username"])
print("Name:", evidence["identity"]["name"])
print("Bio:", evidence["identity"]["bio"])

print("\nPivots:")

for key, value in evidence["analysis"]["pivots"].items():
    print(f"{key}: {value}")