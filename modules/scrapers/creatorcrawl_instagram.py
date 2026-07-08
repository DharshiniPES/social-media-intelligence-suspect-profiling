print("LOADED FILE:", __file__)
import requests


class CreatorCrawlInstagram:

    def __init__(self, api_key):
        self.api_key = api_key
        self.profile_url = "https://creatorcrawl.com/api/instagram/profile"

    def scrape(self, username):

        headers = {
            "x-api-key": self.api_key,
            "accept": "application/json"
        }

        response = requests.get(
            self.profile_url,
            headers=headers,
            params={
                "handle": username
            },
            timeout=60
        )

        response.raise_for_status()

        response_json = response.json()
       

        data = response_json.get("data", {})

        posts = data.get("recent_posts", [])

        profile = {

            "username": data.get("handle"),

            "display_name": data.get("name"),

            "bio": data.get("bio"),

            "url": data.get("url"),

            "profile_picture": (
                data.get("avatar_url")
                or data.get("profile_picture")
                or data.get("profile_pic_url")
                or data.get("avatar")
                or data.get("image")
                or data.get("image_url")
            ),

            "followers": data.get("follower_count"),

            "following": data.get("following_count"),

            "posts_count": data.get("post_count"),

            "verified": data.get("verified"),

            "verified_tier": data.get("verified_tier"),

            "external_url": data.get("external_url"),

            "private": data.get("is_private"),

            "business": data.get("is_business"),

            "platform": data.get("platform"),

            "posts": posts,

            "raw_api": data,

            "status": "Success"

        }

        print("=" * 80)
        print("CreatorCrawl loaded successfully")
        print("Username:", profile["username"])
        print("Posts Found:", len(profile["posts"]))
        print("LOADED FILE:", __file__)
        print("DATA KEYS:", list(data.keys()))
        print("=" * 80)
        import pprint

        pprint.pp(profile["posts"][0])

        return profile
