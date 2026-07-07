"""
SOCMINT Intelligence Pipeline

Author : SOCMINT

Purpose

Normalizes every intelligence source into one
common evidence object.
"""

from modules.pivot_analyzer import extract_advanced_pivots


class IntelligencePipeline:

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # GitHub
    # ---------------------------------------------------------

    def normalize_github(self, github):

        return {

            "source": "GitHub",

            "identity": {

                "username": github.get("username") or "",

                "name": github.get("name") or "",

                "bio": github.get("bio") or ""

            },

            "content": " ".join(

                [

                    github.get("bio") or "",

                    " ".join(

                        repo.get("description") or ""

                        for repo in github.get("repositories", [])

                    )

                ]

            ),

            "metadata": github,

            "status": github.get("status")

        }

    # ---------------------------------------------------------
    # Website
    # ---------------------------------------------------------

    def normalize_website(self, website):

        return {

            "source": "Website",

            "identity": {

                "username": "",

                "name": website.get("title") or "",

                "bio": website.get("description") or ""

            },

            "content": website.get("visible_text") or "",

            "metadata": website,

            "status": website.get("status")

        }

    # ---------------------------------------------------------
    # Instagram
    # ---------------------------------------------------------

    def normalize_instagram(self, instagram):

        content = " ".join([

            instagram.get("display_name") or "",

            instagram.get("bio") or "",

            " ".join(instagram.get("hashtags", [])),

            " ".join(instagram.get("mentions", [])),

            " ".join(instagram.get("emails", [])),

            " ".join(instagram.get("phones", []))

        ])

        return {

            "source": "Instagram",

            "identity": {

                "username": instagram.get("username") or "",

                "name": instagram.get("display_name") or "",

                "bio": instagram.get("bio") or ""

            },

            "content": content,

            "metadata": instagram,

            "status": instagram.get("status")

        }

    # ---------------------------------------------------------
    # Evidence Package
    # ---------------------------------------------------------

    def build_evidence_package(self, normalized):

        return {

            "source": normalized["source"],

            "identity": normalized["identity"],

            "content": normalized["content"],

            "metadata": normalized["metadata"],

            "analysis": {

                "pivots": None,

                "stylometry": None,

                "username_similarity": None,

                "bio_similarity": None,

                "behavior": None,

                "temporal": None

            }

        }

    # ---------------------------------------------------------
    # Pivot Analysis
    # ---------------------------------------------------------

    def run_pivot_analysis(self, evidence):

        pivots = extract_advanced_pivots(

            evidence["content"]

        )

        evidence["analysis"]["pivots"] = pivots

        return evidence

    # ---------------------------------------------------------
    # Run Pipeline
    # ---------------------------------------------------------

    def run(self, normalized):

        evidence = self.build_evidence_package(

            normalized

        )

        evidence = self.run_pivot_analysis(

            evidence

        )

        return evidence