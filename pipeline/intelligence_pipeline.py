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


    def normalize_github(self, github):

        return {

            "source": "GitHub",

            "identity": {

                "username": github.get("username")or "",

                "name": github.get("name")or "",

                "bio": github.get("bio")or ""

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

            "status": github["status"]

        }


    def normalize_website(self, website):

        return {

            "source": "Website",

            "identity": {

                "username": "",

                "name": website.get("title"),

                "bio": website.get("description")

            },

            "content": website.get("visible_text"),

            "metadata": website,

            "status": website.get("status")

        }
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
    def run_pivot_analysis(self, evidence):

        pivots = extract_advanced_pivots(

            evidence["content"]

        )

        evidence["analysis"]["pivots"] = pivots

        return evidence
    def run(self, normalized):

        evidence = self.build_evidence_package(

            normalized

        )

        evidence = self.run_pivot_analysis(

            evidence

        )

        return evidence