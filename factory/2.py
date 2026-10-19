class SQLiteDB:
    def connect(self):
        return " Connected to SQLite"

class PostgreSQLDB:
    def connect(self):
        return "Connected to PostgreSQL"


class DatabaseFactory:

    @staticmethod
    def create(db_type):
        if db_type == "sqlite":
            return SQLiteDB()

        elif db_type == "postgres":
            return PostgreSQLDB()

        else:
            raise ValueError("Unsupported database")

db = DatabaseFactory.create("postgres")

print(db.connect())