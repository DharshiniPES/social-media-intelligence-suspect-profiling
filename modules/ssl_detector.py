import ssl
import socket
from urllib.parse import urlparse


def get_ssl_info(url):

    try:

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        hostname = urlparse(url).netloc

        context = ssl.create_default_context()

        with socket.create_connection((hostname, 443), timeout=10) as sock:

            with context.wrap_socket(
                sock,
                server_hostname=hostname
            ) as ssock:

                cert = ssock.getpeercert()

        return {

            "issuer": ", ".join(
                value
                for item in cert["issuer"]
                for key, value in item
            ),

            "subject": ", ".join(
                value
                for item in cert["subject"]
                for key, value in item
            ),

            "valid_from": cert.get("notBefore"),

            "valid_until": cert.get("notAfter"),

            "version": cert.get("version")

        }

    except Exception:

        return {}