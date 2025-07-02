import sqlite3


class SqliteDatabase:
    def __init__(self, db_file: str = "data/montreal.db"):
        # path to the sqlite file
        self.db_file = db_file
        # open the connection
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row

    @property
    def name(self) -> str:
        return "sqlite"

    @property
    def collection_name(self) -> list[str]:
        # sqlite connection create in __init__
        cursor = self.conn.cursor()  # cursor is used to execute sql queries
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [row[0] for row in cursor.fetchall()]

    def create_table(self, table: str, schema: str) -> None:
        cursor = self.conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({schema})")
        self.conn.commit()

    def insert(self, table: str, data: dict) -> int:
        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        cursor = self.conn.cursor()
        cursor.execute(
            f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
            tuple(data.values()),
        )
        self.conn.commit()
        return cursor.lastrowid

    def fetch_all(self, table: str) -> list[dict]:
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def close(self):
        self.conn.close()
