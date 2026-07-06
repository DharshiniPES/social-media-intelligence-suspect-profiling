from pprint import pprint

from modules.scrapers.github_scraper import GitHubScraper
from pipeline.intelligence_pipeline import IntelligencePipeline

scraper = GitHubScraper()

pipeline = IntelligencePipeline()

github = scraper.scrape("torvalds")

normalized = pipeline.normalize_github(

    github

)

evidence = pipeline.run(

    normalized

)

print()

print("PIVOT ANALYSIS")

pprint(

    evidence["analysis"]["pivots"]

)