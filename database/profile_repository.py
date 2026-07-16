import sqlite3
import json

from core.evidence_model import EvidenceProfile


class ProfileRepository:

    def __init__(self):

        self.conn = sqlite3.connect(
            "database/socmint.db"
        )

        self.cursor = self.conn.cursor()

    def save(self, profile: EvidenceProfile):

        self.cursor.execute(
            """
            INSERT INTO profiles
            (
                username,
                platform,
                display_name,
                bio,
                profile_url,
                raw_data
            )

            VALUES (?, ?, ?, ?, ?, ?)
            """,

            (

                profile.username,

                profile.platform,

                profile.display_name,

                profile.bio,

                profile.profile_url,

                json.dumps(profile.raw_data)

            )

        )

        self.conn.commit()

    def get_all(self):

        self.cursor.execute(

            "SELECT * FROM profiles"

        )

        return self.cursor.fetchall()