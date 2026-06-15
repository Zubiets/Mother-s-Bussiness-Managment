import sqlite3

class Inventory:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            print(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from database")

    def execute_query(self, query, params=None):
        if not self.connection:
            print("No database connection")
            return None
        
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None
    
def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        );
        """
        self.execute_query(create_table_query)