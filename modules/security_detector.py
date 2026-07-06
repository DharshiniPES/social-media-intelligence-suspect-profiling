import requests


def analyze_security(url):

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:

        r = requests.get(url, timeout=10)

        headers = r.headers

        return {

            "HTTPS": url.startswith("https://"),

            "HSTS": "Strict-Transport-Security" in headers,

            "CSP": "Content-Security-Policy" in headers,

            "X-Frame-Options": "X-Frame-Options" in headers,

            "X-Content-Type": "X-Content-Type-Options" in headers,

            "Referrer-Policy": "Referrer-Policy" in headers,

            "Permissions-Policy": "Permissions-Policy" in headers

        }

    except:

        return {}