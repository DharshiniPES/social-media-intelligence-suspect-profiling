from modules.scrapers.instagram_collector import InstagramCollector
from modules.scrapers.github_scraper import GitHubScraper
from modules.scrapers.website_scraper import WebsiteScraper

from pipeline.normalizer import (
    normalize_instagram,
    normalize_github,
    normalize_website,
)

from database.candidate_repository import CandidateRepository


class SearchPipeline:

    @staticmethod
    def search(username, platforms):

        repo = CandidateRepository()

        candidates = []

        # ----------------------------------------
        # Instagram
        # ----------------------------------------
        if "Instagram" in platforms:

            try:

                result = InstagramCollector().scrape(username)

                if result:

                    profile = normalize_instagram(result)

                    repo.save(profile)

                    candidates.append(profile)

            except Exception as e:

                print("Instagram:", e)

        # ----------------------------------------
        # GitHub
        # ----------------------------------------
        if "GitHub" in platforms:

            try:

                result = GitHubScraper().scrape(username)

                if result.get("status") == "success":

                    profile = normalize_github(result)

                    repo.save(profile)

                    candidates.append(profile)

            except Exception as e:

                print("GitHub:", e)

        # ----------------------------------------
        # Website
        # ----------------------------------------
        if "Website" in platforms:

            try:

                result = WebsiteScraper().scrape(username)

                if result:

                    profile = normalize_website(result)

                    repo.save(profile)

                    candidates.append(profile)

            except Exception as e:

                print("Website:", e)

        return candidates