from database.db_manager import DatabaseManager

db = DatabaseManager()

db.create_tables()

print("Database Created")