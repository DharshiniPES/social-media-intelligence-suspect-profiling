
from modules.scrapers.creatorcrawl_instagram import CreatorCrawlInstagram

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("CREATORCRAWL_API_KEY")

scraper = CreatorCrawlInstagram(API_KEY)

profile = scraper.scrape("instagram")

import json

print(json.dumps(profile, indent=4))