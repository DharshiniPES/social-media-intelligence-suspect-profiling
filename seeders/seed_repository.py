from database.candidate_repository import CandidateRepository

from modules.scrapers.github_scraper import GitHubScraper
from modules.scrapers.website_scraper import WebsiteScraper
from modules.scrapers.instagram_collector import InstagramCollector

from pipeline.normalizer import (
    normalize_github,
    normalize_instagram,
    normalize_website,
)

repo = CandidateRepository()
github = GitHubScraper()

with open(
    "datasets/seed/github_usernames.txt"
) as f:

    usernames = [

        x.strip()

        for x in f.readlines()

        if x.strip()

    ]

for username in usernames:

    print("GitHub:", username)

    try:

        data = github.scrape(username)

        if data["status"] == "success":

            profile = normalize_github(data)

            repo.save(profile)

    except Exception as e:

        print(e)