import sqlite3

conn = sqlite3.connect("database/socmint.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS identity_repository (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT,

    platform TEXT,

    display_name TEXT,

    bio TEXT,

    profile_url TEXT,

    followers INTEGER,

    following INTEGER,

    posts_count INTEGER,

    emails TEXT,

    hashtags TEXT,

    hyperlinks TEXT,

    timestamps TEXT,

    raw_data TEXT

)
""")

conn.commit()

conn.close()

print("Identity Repository Created Successfully!")