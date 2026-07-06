"""
GitHub Intelligence Scraper
Uses the GitHub public API.
"""

import requests


class GitHubScraper:

    BASE_URL = "https://api.github.com/users"

    def scrape(self, username):

        try:

            response = requests.get(
                f"{self.BASE_URL}/{username}",
                timeout=10
            )

            if response.status_code != 200:
                return {
                    "status": "failed",
                    "message": "User not found"
                }

            data = response.json()
            try:
                repositories = self.get_repositories(username)
            except Exception as e:
                print("Repository Error:", e)
                repositories = []
            statistics = self.calculate_statistics(repositories)
            summary = self.generate_summary(
                data,
                statistics
            )
            community_score = self.calculate_community_score(
                data,
                statistics
            )
            return {

                "status": "success",

                "source": "GitHub",

                "username": data.get("login"),

                "name": data.get("name"),

                "bio": data.get("bio"),

                "company": data.get("company"),

                "location": data.get("location"),

                "blog": data.get("blog"),

                "email": data.get("email"),

                "followers": data.get("followers"),

                "following": data.get("following"),

                "public_repos": data.get("public_repos"),

                "repositories": repositories,

                "statistics": statistics,

                "avatar": data.get("avatar_url"),

                "profile_url": data.get("html_url"),

                "community_score": community_score,

                "summary": summary,

            }

        except Exception as e:
            
            return {

                "status": "failed",

                "message": str(e)

            }
    def get_repositories(self, username):

        try:

            response = requests.get(
                f"{self.BASE_URL}/{username}/repos",
                timeout=10
            )

            if response.status_code != 200:
                return []

            repositories = []

            for repo in response.json():

                repositories.append({

                    "name": repo.get("name"),

                    "description": repo.get("description"),

                    "language": repo.get("language"),

                    "stars": repo.get("stargazers_count"),

                    "forks": repo.get("forks_count"),

                    "topics": repo.get("topics", [])

                })

            return repositories

        except Exception:

            return []
    def calculate_statistics(self, repositories):

        total_stars = 0

        total_forks = 0

        languages = {}

        most_starred = None

        for repo in repositories:

            total_stars += repo["stars"]

            total_forks += repo["forks"]

            language = repo["language"]

            if language:

                languages[language] = languages.get(language, 0) + 1

            if most_starred is None:

                most_starred = repo

            elif repo["stars"] > most_starred["stars"]:

                most_starred = repo

        top_language = None

        if languages:

            top_language = max(
                languages,
                key=languages.get
            )

        return {

            "repo_count": len(repositories),

            "total_stars": total_stars,

            "total_forks": total_forks,

            "top_language": top_language,

            "most_starred": most_starred

        }
    def generate_summary(self, data, statistics):

        summary = []

        summary.append(
            f"GitHub user {data.get('login')} has {statistics['repo_count']} public repositories."
        )

        summary.append(
            f"The account has {data.get('followers')} followers and follows {data.get('following')} users."
        )

        if statistics["top_language"]:

            summary.append(
                f"Most frequently used language is {statistics['top_language']}."
            )

        if statistics["most_starred"]:

            summary.append(
                f"Most starred repository is '{statistics['most_starred']['name']}' "
                f"with {statistics['most_starred']['stars']} stars."
            )

        summary.append(
            f"Total stars across repositories: {statistics['total_stars']}."
        )

        summary.append(
            f"Total forks across repositories: {statistics['total_forks']}."
        )

        return " ".join(summary)
    def calculate_community_score(self, data, statistics):

        score = 0

        score += min(data.get("followers", 0) / 1000, 40)

        score += min(statistics["total_stars"] / 10000, 40)

        score += min(statistics["repo_count"], 20)

        return round(score, 2)