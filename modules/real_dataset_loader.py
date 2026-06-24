import pandas as pd
import re

class RealDatasetLoader:

    def __init__(self, filepath):
        self.filepath = filepath

    def load_profiles(self, limit=100):

        df = pd.read_csv(self.filepath)

        profiles = []

        for _, row in df.head(limit).iterrows():

            timestamp = str(row["Created At"])

            try:
                hour = int(
                    timestamp.split(" ")[1].split(":")[0]
                )
            except:
                hour = 0
            tweet = str(row["Tweet"])

            hashtags = re.findall(r"#(\w+)", tweet)

            links = re.findall(
                r"https?://[^\s]+",
                tweet
            )
            emojis=[]

            profile = {

                "id": str(row["User ID"]),

                "username": str(row["Username"]),

                "bio": "",

                "posts": tweet,

                "hashtags": hashtags,

                "links": links,

                "emojis": emojis,

                "timestamps": [timestamp],

                "active_hours": [hour],
                "followers": int(row["Follower Count"]),
                "retweets": int(row["Retweet Count"]),
                "verified": bool(row["Verified"]),

                "bot_label": int(row["Bot Label"])
            }

            profiles.append(profile)

        return profiles