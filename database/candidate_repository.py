import sqlite3
import json

from core.evidence_model import EvidenceProfile


class CandidateRepository:

    def __init__(self):

        self.conn = sqlite3.connect(
            "database/socmint.db",
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()
    def save(self, profile: EvidenceProfile):

        # ----------------------------------------
        # Check whether profile already exists
        # ----------------------------------------

        self.cursor.execute(
            """
            SELECT id

            FROM identity_repository

            WHERE username = ?

            AND platform = ?
            """,

            (
                profile.username,
                profile.platform
            )
        )

        existing = self.cursor.fetchone()

        # ----------------------------------------
        # UPDATE existing profile
        # ----------------------------------------

        if existing:

            self.cursor.execute(
                """
                UPDATE identity_repository

                SET

                    display_name = ?,

                    bio = ?,

                    profile_url = ?,

                    followers = ?,

                    following = ?,

                    posts_count = ?,

                    emails = ?,

                    hashtags = ?,

                    hyperlinks = ?,

                    timestamps = ?,

                    raw_data = ?

                WHERE id = ?
                """,

                (

                    profile.display_name,

                    profile.bio,

                    profile.profile_url,

                    profile.followers,

                    profile.following,

                    profile.posts_count,

                    json.dumps(profile.emails),

                    json.dumps(profile.hashtags),

                    json.dumps(profile.hyperlinks),

                    json.dumps(profile.timestamps),

                    json.dumps(profile.raw_data),

                    existing[0]

                )

            )

            print(
                f"Updated: {profile.username} ({profile.platform})"
            )

        # ----------------------------------------
        # INSERT new profile
        # ----------------------------------------

        else:

            self.cursor.execute(
                """
                INSERT INTO identity_repository
                (
                    username,
                    platform,
                    display_name,
                    bio,
                    profile_url,
                    followers,
                    following,
                    posts_count,
                    emails,
                    hashtags,
                    hyperlinks,
                    timestamps,
                    raw_data
                )

                VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,

                (

                    profile.username,

                    profile.platform,

                    profile.display_name,

                    profile.bio,

                    profile.profile_url,

                    profile.followers,

                    profile.following,

                    profile.posts_count,

                    json.dumps(profile.emails),

                    json.dumps(profile.hashtags),

                    json.dumps(profile.hyperlinks),

                    json.dumps(profile.timestamps),

                    json.dumps(profile.raw_data)

                )

            )

            print(
                f"Inserted: {profile.username} ({profile.platform})"
            )

        self.conn.commit()
    def get_all(self):

        self.cursor.execute(
            """
            SELECT *

            FROM identity_repository
            """
        )

        rows = self.cursor.fetchall()

        profiles = []

        for row in rows:

            profile = EvidenceProfile()

            profile.username = row[1]

            profile.platform = row[2]

            profile.display_name = row[3]

            profile.bio = row[4]

            profile.profile_url = row[5]

            profile.followers = row[6]

            profile.following = row[7]

            profile.posts_count = row[8]

            profile.emails = json.loads(row[9])

            profile.hashtags = json.loads(row[10])

            profile.hyperlinks = json.loads(row[11])

            profile.timestamps = json.loads(row[12])

            profile.raw_data = json.loads(row[13])

            profiles.append(profile)

        return profiles
    def count(self):

        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM identity_repository
            """
        )

        return self.cursor.fetchone()[0]
    def search_username(self, username):

        self.cursor.execute(

            """
            SELECT *
            FROM identity_repository

            WHERE username LIKE ?
            """,

            (f"%{username}%",)

        )

        return self.cursor.fetchall()   
    def search_platform(self, platform):

        self.cursor.execute(

            """
            SELECT *

            FROM identity_repository

            WHERE platform=?
            """,

            (platform,)

        )

        return self.cursor.fetchall()
    def delete(self, id):

        self.cursor.execute(

            """
            DELETE

            FROM identity_repository

            WHERE id=?
            """,

            (id,)

        )

        self.conn.commit()
        
    def get_all_profiles(self):
        return self.get_all()