import sqlite3

conn = sqlite3.connect("database/socmint.db")

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS profiles(

id INTEGER PRIMARY KEY AUTOINCREMENT,

username TEXT,

platform TEXT,

display_name TEXT,

bio TEXT,

profile_url TEXT,

raw_data TEXT

)

""")

conn.commit()

conn.close()

print("Done")