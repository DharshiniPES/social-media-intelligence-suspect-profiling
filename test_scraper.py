from modules.scrapers.website_scraper import WebsiteScraper

scraper = WebsiteScraper()

result = scraper.scrape("https://example.com")

print("\nSTATUS")
print(result["status"])

print("\nTITLE")
print(result["title"])

print("\nDESCRIPTION")
print(result["description"])

print("\nEMAILS")
print(result["emails"])

print("\nPHONES")
print(result["phones"])

print("\nURLS")
print(result["urls"])

print("\nDEVICES")
print(result["devices"])

print("\nLOCATIONS")
print(result["locations"])

print("\nVISIBLE TEXT")

print(result["visible_text"][:1000])