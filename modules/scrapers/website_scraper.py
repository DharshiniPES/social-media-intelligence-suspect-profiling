"""
Website Intelligence Scraper
SOCMINT Platform
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from modules.technology_detector import detect_technologies
from modules.pivot_analyzer import extract_advanced_pivots
from modules.security_detector import analyze_security
from urllib.parse import urlparse
from modules.risk_analyzer import website_risk
from modules.whois_detector import get_whois
class WebsiteScraper:

    def __init__(self):

        self.headers = {

            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/138.0 Safari/537.36"
            )

        }

    # =========================================================

    def fetch_page(self, url):

        if not url.startswith(("http://", "https://")):

            url = "https://" + url

        response = requests.get(

            url,

            headers=self.headers,

            timeout=15

        )

        response.raise_for_status()

        return response.text, url

    # =========================================================

    def parse_html(self, html):

        return BeautifulSoup(html, "lxml")

    # =========================================================

    def get_title(self, soup):

        if soup.title:

            return soup.title.get_text(strip=True)

        return ""

    # =========================================================

    def get_description(self, soup):

        meta = soup.find(

            "meta",

            attrs={"name": "description"}

        )

        if meta:

            return meta.get("content", "")

        return ""

    # =========================================================

    def get_visible_text(self, soup):

        for tag in soup(

            [

                "script",

                "style",

                "noscript",

                "svg"

            ]

        ):

            tag.decompose()

        text = soup.get_text(separator=" ")

        return " ".join(text.split())

    # =========================================================

    def extract_links(self, soup, base_url):

        links = []

        for a in soup.find_all("a", href=True):

            href = urljoin(base_url, a["href"])

            links.append(href)

        return list(set(links))

    # =========================================================

    def extract_images(self, soup, base_url):

        images = []

        for img in soup.find_all("img"):

            src = img.get("src")

            if src:

                images.append(

                    urljoin(base_url, src)

                )

        return list(set(images))

    # =========================================================

    def extract_social_links(self, links):

        social = []

        keywords = [

            "instagram",

            "facebook",

            "twitter",

            "x.com",

            "linkedin",

            "youtube",

            "github",

            "telegram"

        ]

        for link in links:

            if any(

                word in link.lower()

                for word in keywords

            ):

                social.append(link)

        return social

    # =========================================================

    def get_open_graph_image(self, soup):

        og = soup.find(

            "meta",

            property="og:image"

        )

        if og:

            return og.get(

                "content",

                ""

            )

        return ""

    # =========================================================

    def scrape(self, url):

        try:

            html, final_url = self.fetch_page(url)

            soup = self.parse_html(html)

            title = self.get_title(soup)

            description = self.get_description(soup)

            visible_text = self.get_visible_text(soup)

            pivots = extract_advanced_pivots(visible_text)

            links = self.extract_links(

                soup,

                final_url

            )

            images = self.extract_images(

                soup,

                final_url

            )

            social = self.extract_social_links(

                links

            )
            
            technologies = detect_technologies(html)
            og_image = self.get_open_graph_image(

                soup

            )
            security = analyze_security(final_url)
            whois_info = get_whois(final_url)
            internal, external = self.classify_links(

                links,

                final_url

            )
            links = self.extract_links(
                soup,
                final_url
            )


            return {

                "status": "success",

                "source": "Website",

                "title": title,

                "description": description,

                "visible_text": visible_text,

                "emails": pivots["emails"],

                "phones": pivots["phones"],

                "urls": links,

                "devices": pivots["devices"],

                "locations": pivots["locations"],

                "images": images,

                "social_links": social,

                "open_graph_image": og_image,

                "html": html,

                "technologies": technologies,

                "security": security,

                "internal_links": internal,

                "external_links": external,

                "whois": whois_info,

            }

        except Exception as e:

            return {

                "status": "failed",

                "message": str(e)

            }
    def classify_links(self, links, base):

        domain = urlparse(base).netloc

        internal = []

        external = []

        for link in links:

            if urlparse(link).netloc == domain:

                internal.append(link)

            else:

                external.append(link)

        return internal, external

