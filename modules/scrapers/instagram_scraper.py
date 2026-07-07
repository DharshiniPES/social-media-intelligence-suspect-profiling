from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import json

class InstagramScraper:

    def __init__(self, headless=True):
        self.headless = headless

    def scrape(self, username):
        """
        Scrape a public Instagram profile using Playwright.
        Returns structured intelligence.
        """

        url = f"https://www.instagram.com/{username}/"

        result = {
            "username": username,
            "url": url,

            "page_title": None,
            "meta_description": None,

            "profile_picture": None,
            "canonical_url": None,

            "display_name": None,
            "bio": None,

            "followers": None,
            "following": None,
            "posts_count": None,

            "emails": [],
            "phones": [],

            "public_links": [],
            "external_links": [],
            "posts": [],
            "structured_data": {},
            "metadata": {},
            "raw_html": None,

            "status": "Success"
        }

        try:
            with sync_playwright() as p:

                browser = p.chromium.launch(
                    headless=self.headless
                )

                page = browser.new_page()

                page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=60000
                )

                # Give Instagram a few seconds to render
                page.wait_for_timeout(5000)

                html = page.content()

                browser.close()

            result["raw_html"] = html

            soup = BeautifulSoup(html, "html.parser")
            # -------------------------------------------------
            # Attempt to extract embedded JSON
            # -------------------------------------------------

            json_scripts = soup.find_all(
                "script",
                type="application/ld+json"
            )

            for script in json_scripts:

                try:

                    data = json.loads(script.string)

                    if isinstance(data, dict):

                        result["structured_data"] = data

                except Exception:

                    pass
            # -----------------------------
            # Collect All Meta Tags
            # -----------------------------
            metadata = {}

            for tag in soup.find_all("meta"):

                key = (
                    tag.get("property")
                    or tag.get("name")
                    or tag.get("itemprop")
                )

                value = tag.get("content")

                if key and value:
                    metadata[key] = value

            result["metadata"] = metadata
            # -----------------------------
            # Page Title
            # -----------------------------
            if soup.title:
                result["page_title"] = soup.title.get_text(strip=True)

            # -----------------------------
            # Meta Description
            # -----------------------------
            description = soup.find(
                "meta",
                attrs={"name": "description"}
            )

            if description:
                result["meta_description"] = description.get("content")

            # -----------------------------
            # OpenGraph Image
            # -----------------------------
            og_image = soup.find(
                "meta",
                attrs={"property": "og:image"}
            )

            if og_image:
                result["profile_picture"] = og_image.get("content")

            # -----------------------------
            # Canonical URL
            # -----------------------------
            canonical = soup.find(
                "link",
                rel="canonical"
            )

            if canonical:
                result["canonical_url"] = canonical.get("href")

            # -----------------------------
            # Public Links
            # -----------------------------
            links = set()

            for a in soup.find_all("a", href=True):

                href = a["href"]

                if href.startswith("http"):
                    links.add(href)

            result["public_links"] = sorted(list(links))

            # -----------------------------
            # External Website Detection
            # -----------------------------
            result["external_links"] = [
                link
                for link in result["public_links"]
                if "instagram.com" not in link.lower()
            ]
            post_links = []

            for link in result["public_links"]:

                if "/p/" in link:

                    post_links.append(link)

            result["posts"] = sorted(
                list(set(post_links))
            )
            # -----------------------------
            # Email Extraction
            # -----------------------------
            emails = set(
                re.findall(
                    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                    html
                )
            )

            result["emails"] = sorted(list(emails))

            # Instagram does not expose public phone numbers reliably
            result["phones"] = []

            # -----------------------------
            # Visible Text
            # -----------------------------
            result["visible_text"] = soup.get_text(
                separator=" ",
                strip=True
            )

            # -----------------------------
            # Parse Open Graph Title
            # -----------------------------
            og_title = result["metadata"].get("og:title", "")

            if "(@" in og_title:
                try:
                    result["display_name"] = og_title.split("(@")[0].strip()
                    result["username"] = (
                        og_title.split("(@")[1]
                        .split(")")[0]
                        .strip()
                    )
                except Exception:
                    pass

            # -----------------------------
            # Parse Description
            # -----------------------------
            description = result["metadata"].get("description", "")

            if description:

                try:

                    stats = re.search(
                        r'([\d.,MK]+)\s+Followers,\s+([\d.,MK]+)\s+Following,\s+([\d.,MK]+)\s+Posts',
                        description
                    )

                    if stats:
                        result["followers"] = stats.group(1)
                        result["following"] = stats.group(2)
                        result["posts_count"] = stats.group(3)

                    bio_match = re.search(
                        r':\s*"([^"]+)"',
                        description
                    )

                    if bio_match:
                        result["bio"] = bio_match.group(1)

                except Exception:
                    pass

            return result
        except Exception as e:

            result["status"] = f"Error: {str(e)}"
            return result