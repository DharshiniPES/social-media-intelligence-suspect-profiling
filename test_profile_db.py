from database.profile_repository import ProfileRepository

from modules.scrapers.instagram_collector import InstagramCollector

from pipeline.normalizer import normalize_instagram

repo = ProfileRepository()

raw = InstagramCollector().scrape("instagram")

profile = normalize_instagram(raw)

repo.save(profile)

print(repo.get_all())