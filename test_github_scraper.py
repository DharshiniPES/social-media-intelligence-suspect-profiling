from modules.scrapers.github_scraper import GitHubScraper

scraper = GitHubScraper()

result = scraper.scrape("torvalds")

print()

print(result["summary"])