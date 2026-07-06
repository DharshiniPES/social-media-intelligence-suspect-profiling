import whois
from urllib.parse import urlparse


def get_whois(url):

    try:

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        domain = urlparse(url).netloc

        info = whois.whois(domain)

        return {

            "domain": domain,

            "registrar": info.registrar,

            "creation_date": str(info.creation_date),

            "expiration_date": str(info.expiration_date),

            "organization": info.org,

            "country": info.country,

            "name_servers": info.name_servers

        }

    except Exception:

        return {}