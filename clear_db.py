import sqlite3

conn = sqlite3.connect(
    "database/socmint.db"
)

cursor = conn.cursor()

cursor.execute(
    "DELETE FROM comparisons"
)

conn.commit()

print("Database cleared.")