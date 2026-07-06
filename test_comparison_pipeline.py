from pprint import pprint

from modules.scrapers.github_scraper import GitHubScraper

from pipeline.intelligence_pipeline import IntelligencePipeline

from pipeline.comparison_pipeline import ComparisonPipeline


scraper = GitHubScraper()

pipeline = IntelligencePipeline()

comparison = ComparisonPipeline()


user1 = pipeline.run(

    pipeline.normalize_github(

        scraper.scrape("torvalds")

    )

)

user2 = pipeline.run(

    pipeline.normalize_github(

        scraper.scrape("octocat")

    )

)


result = comparison.compare(

    user1,

    user2

)

print("\nComparison Results\n")

for key, value in result.items():

    print(f"{key:25} : {value}")