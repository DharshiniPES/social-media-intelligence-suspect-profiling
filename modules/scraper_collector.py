import requests
from bs4 import BeautifulSoup
import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

def live_scrape_profile(target_url):
    """Scrapes actual public page layouts live."""
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        response = requests.get(target_url, headers=headers, timeout=5)
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get actual page title
        title = soup.find("title")
        title_text = title.string.strip() if title else "No Title Found"
        
        # Fallback to look for body snippet text if meta description is missing
        bio_tag = soup.find("meta", property="og:description") or soup.find("meta", name="description")
        if bio_tag and bio_tag.get("content"):
            bio_text = bio_tag["content"].strip()
        else:
            bio_text = soup.body.get_text()[:300].strip() if soup.body else "No Bio Text Isolated"
            
        return {
            "scraped_name": title_text,
            "scraped_bio": bio_text
        }
    except Exception as e:
        print(f"Scraper error: {e}")
        return None