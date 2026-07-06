"""
Adapters

Converts intelligence collected from different
sources into a common profile format.
"""


def github_to_profile(github):

    text = github.get("summary", "")

    return {

        "posts": text,

        "active_hours": [12],

        "hashtags": []

    }