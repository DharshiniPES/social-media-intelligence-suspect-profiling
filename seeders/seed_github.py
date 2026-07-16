import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)
from database.candidate_repository import CandidateRepository
from modules.scrapers.github_scraper import GitHubScraper
from pipeline.normalizer import normalize_github

repo = CandidateRepository()
scraper = GitHubScraper()

with open("datasets/seed/github_usernames.txt", "r", encoding="utf-8") as f:
    usernames = [u.strip() for u in f if u.strip()]

success = 0
failed = 0

for username in usernames:

    print(f"Fetching {username}")

    try:
        data = scraper.scrape(username)

        if data.get("status") == "success":
            profile = normalize_github(data)
            repo.save(profile)
            success += 1
        else:
            print(f"Skipped: {username}")
            failed += 1

    except KeyboardInterrupt:
        print("\nSeeding stopped by user.")
        break

    except Exception as e:
        print(f"Error for {username}: {e}")
        failed += 1
        continue
print()
print("=" * 40)
print("Completed")
print("Success:", success)
print("Failed :", failed)