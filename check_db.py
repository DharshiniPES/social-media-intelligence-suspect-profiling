from database.db_manager import DatabaseManager

db = DatabaseManager()

rows = db.get_comparisons()

print("Total Rows:", len(rows))

for row in rows:
    print(row)