from modules.search.search_manager import SearchManager

# Import your real collectors
from modules.collectors.instagram_collector import InstagramCollector
from modules.collectors.github_collector import GithubCollector
from modules.collectors.website_collector import WebsiteCollector

manager = SearchManager()

manager.register_platform(
    "instagram",
    InstagramCollector()
)

manager.register_platform(
    "github",
    GithubCollector()
)

manager.register_platform(
    "website",
    WebsiteCollector()
)

results = manager.search(

    query="instagram",

    platforms=[
        "instagram",
        "github",
        "website"
    ]
)

print()

print("=" * 60)

print("Candidates Found")

print("=" * 60)

for r in results:

    print(r.identity.username)