import re
from urllib.parse import urlparse


class InstagramIntelligence:

    def analyze(self, profile):

        intelligence = profile.copy()

        text = profile.get("visible_text", "")

        # -------------------------------------------------
        # Preserve Profile Information
        # -------------------------------------------------

        intelligence["display_name"] = profile.get("display_name")
        intelligence["bio"] = profile.get("bio")
        intelligence["followers"] = profile.get("followers")
        intelligence["following"] = profile.get("following")
        intelligence["posts_count"] = profile.get("posts_count")
        intelligence["profile_picture"] = profile.get("profile_picture")

        # -------------------------------------------------
        # Email Extraction
        # -------------------------------------------------

        emails = sorted(set(
            re.findall(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                text
            )
        ))

        intelligence["emails"] = emails

        # -------------------------------------------------
        # Instagram does not reliably expose phone numbers
        # -------------------------------------------------

        intelligence["phones"] = []

        # -------------------------------------------------
        # Hashtags
        # -------------------------------------------------

        hashtags = sorted(set(
            re.findall(
                r"#(\w+)",
                text
            )
        ))

        intelligence["hashtags"] = hashtags

        # -------------------------------------------------
        # Mentions
        # -------------------------------------------------

        mentions = sorted(set(
            re.findall(
                r"@([A-Za-z0-9_.]+)",
                text
            )
        ))

        intelligence["mentions"] = mentions

        # -------------------------------------------------
        # External Domains
        # -------------------------------------------------

        domains = []

        for link in intelligence.get("external_links", []):

            try:

                domain = urlparse(link).netloc

                if domain:
                    domains.append(domain)

            except Exception:
                pass

        intelligence["external_domains"] = sorted(set(domains))

        # -------------------------------------------------
        # Risk Indicators
        # -------------------------------------------------

        suspicious_words = [

            "hack",
            "fraud",
            "crypto",
            "bitcoin",
            "drugs",
            "weapon",
            "exploit",
            "malware",
            "phishing",
            "telegram"

        ]

        searchable_text = (
            (intelligence.get("bio") or "")
            + " "
            + text
        ).lower()

        risk_flags = []

        for word in suspicious_words:

            if word in searchable_text:

                risk_flags.append(word)

        intelligence["risk_flags"] = sorted(set(risk_flags))

        # -------------------------------------------------
        # Intelligence Score
        # -------------------------------------------------

        score = 0

        score += len(emails) * 10
        score += len(intelligence["external_domains"]) * 5
        score += len(hashtags)
        score += len(mentions)
        score += len(risk_flags) * 5

        intelligence["intelligence_score"] = score

        # -------------------------------------------------
        # Summary
        # -------------------------------------------------

        intelligence["summary"] = {

            "followers": intelligence.get("followers"),
            "following": intelligence.get("following"),
            "posts": intelligence.get("posts_count"),

            "emails": len(emails),
            "hashtags": len(hashtags),
            "mentions": len(mentions),
            "domains": len(intelligence["external_domains"]),
            "risk_flags": len(risk_flags)

        }

        return intelligence