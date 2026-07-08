from modules.scrapers.creatorcrawl_instagram import CreatorCrawlInstagram
from modules.scrapers.instagram_scraper import InstagramScraper


class InstagramCollector:

    def __init__(self, api_key=None):
        self.api_key = api_key

    def scrape(self, username):

        if self.api_key:
            try:
                scraper = CreatorCrawlInstagram(self.api_key)
                return scraper.scrape(username)

            except Exception:
                pass

        scraper = InstagramScraper()
        return scraper.scrape(username)