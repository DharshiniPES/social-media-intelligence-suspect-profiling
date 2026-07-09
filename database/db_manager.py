import sqlite3

class DatabaseManager:

    def __init__(self, db_name="database/socmint.db"):
        # 🔑 FIXED: check_same_thread=False allows Streamlit's multi-threaded runtime
        # to query this database layout without throwing a ProgrammingError.
        self.conn = sqlite3.connect(db_name, check_same_thread=False)

    def create_tables(self):
        cursor = self.conn.cursor()  # Spawn a fresh, thread-safe cursor
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS comparisons(

                pair_id INTEGER PRIMARY KEY AUTOINCREMENT,

                profile1 TEXT,
                profile2 TEXT,

                username_score REAL,
                bio_score REAL,
                stylometry_score REAL,
                emoji_score REAL,
                temporal_score REAL,
                hyperlink_score REAL,
                hashtag_score REAL,
                behavior_score REAL,
                fusion_score REAL,
                explanation TEXT,

                linked INTEGER
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS investigator_notes(

                note_id INTEGER PRIMARY KEY AUTOINCREMENT,

                account_id TEXT,

                note TEXT
            )
            """
        )

        self.conn.commit()

    def insert_comparison(
        self,
        profile1,
        profile2,
        username_score,
        bio_score,
        stylometry_score,
        emoji_score,
        temporal_score,
        hyperlink_score,
        hashtag_score,
        behavior_score,   
        fusion_score,
        explanation,
        linked
    ):
        cursor = self.conn.cursor()  # Spawn a fresh, thread-safe cursor
        cursor.execute(
            """
            INSERT INTO comparisons(

                profile1,
                profile2,

                username_score,
                bio_score,
                stylometry_score,
                emoji_score,
                temporal_score,
                hyperlink_score,
                hashtag_score,
                behavior_score,
                fusion_score,

                explanation,

                linked

            )

            VALUES(
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                profile1,
                profile2,
                float(username_score),
                float(bio_score),
                float(stylometry_score),
                float(emoji_score),
                float(temporal_score),
                float(hyperlink_score),
                float(hashtag_score),
                float(behavior_score),
                float(fusion_score),
                str(explanation),
                int(linked)
            )
        )

        self.conn.commit()

    def get_comparisons(self):
        cursor = self.conn.cursor()  # Spawn a fresh, thread-safe cursor
        cursor.execute(
            """
            SELECT *
            FROM comparisons
            """
        )

        return cursor.fetchall()

    def save_note(self, account_id, note):
        cursor = self.conn.cursor()  # Spawn a fresh, thread-safe cursor
        cursor.execute(
            """
            INSERT INTO investigator_notes(

                account_id,

                note

            )

            VALUES(?, ?)
            """,
            (
                account_id,
                note
            )
        )

        self.conn.commit()

    def get_notes(self):
        cursor = self.conn.cursor()  # Spawn a fresh, thread-safe cursor
        cursor.execute(
            """
            SELECT *
            FROM investigator_notes
            """
        )

        return cursor.fetchall()