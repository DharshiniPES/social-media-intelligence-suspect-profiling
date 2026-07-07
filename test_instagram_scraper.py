from modules.scrapers.instagram_scraper import InstagramScraper

scraper = InstagramScraper()

# Scrape Instagram profile
result = scraper.scrape("instagram")

print("\n===== RESULT =====\n")

for key, value in result.items():
    if key == "raw_html":
        if value:
            print(f"{key}: <{len(value)} characters>")
        else:
            print(f"{key}: None")
    else:
        print(f"{key}: {value}")
print("\n===== METADATA =====")

for key, value in result["metadata"].items():
    print(f"{key}: {value}")