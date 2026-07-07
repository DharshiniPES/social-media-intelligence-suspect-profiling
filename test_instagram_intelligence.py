from modules.scrapers.instagram_scraper import InstagramScraper
from dashboard.instagram_intelligence import InstagramIntelligence

scraper = InstagramScraper()
profile = scraper.scrape("instagram")

intel = InstagramIntelligence().analyze(profile)

print("\n========== SUMMARY ==========\n")

for key, value in intel["summary"].items():
    print(f"{key}: {value}")

print("\nRisk Flags:")
print(intel["risk_flags"])

print("\nExternal Domains:")
print(intel["external_domains"])

print("\nIntelligence Score:")
print(intel["intelligence_score"])