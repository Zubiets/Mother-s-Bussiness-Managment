import sqlite3

# model to manipulate the database with code
class Database:
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
        
    def create_table(self, table_name, columns):
        columns_str = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
        self.execute_query(query)
        
    def insert_item(self, table_name, item_data):
        columns = ", ".join(item_data.keys())
        placeholders = ", ".join(["?" for _ in item_data])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.execute_query(query, tuple(item_data.values()))
    
    def get_items(self, table_name):
        query = f"SELECT * FROM {table_name}"
        return self.execute_query(query)
    
    def delete_item(self, table_name, item_id):
        query = f"DELETE FROM {table_name} WHERE id = ?"
        self.execute_query(query, (item_id,))

inventory = Database('data/inventory.db')
inventory.connect()
def create_tables():
    # create the tables using the database model
    inventory.create_table('product_categories', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'supplier_id': 'INTEGER NOT NULL',
        'description': 'TEXT',
        'FOREIGN KEY(supplier_id)': 'REFERENCES suppliers(id)'
    })

    inventory.create_table('suppliers', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'contact_info': 'TEXT NOT NULL'
    })

    inventory.create_table('products', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'category_id': 'INTEGER NOT NULL',
        'name': 'TEXT NOT NULL',
        'quantity': 'INTEGER NOT NULL',
        'price': 'REAL NOT NULL',
        'qr_code': 'TEXT NOT NULL',
        'FOREIGN KEY(category_id)': 'REFERENCES sales_categories(id)'
    })

    inventory.create_table('sales', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'product_id': 'INTEGER NOT NULL',
        'quantity': 'INTEGER NOT NULL',
        'discount': 'REAL NOT NULL',
        'total_price': 'REAL NOT NULL',
        'date': 'TEXT NOT NULL',
        'FOREIGN KEY(product_id)': 'REFERENCES products(id)'
    })

    inventory.create_table('users', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'username': 'TEXT NOT NULL',
        'email': 'TEXT NOT NULL',
        'password': 'TEXT NOT NULL'
    })

    inventory.create_table('employees', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'salary': 'REAL NOT NULL',
        'phone': 'TEXT'
    })

    inventory.create_table('time_working', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'employee_id': 'INTEGER NOT NULL',
        'date': 'TEXT NOT NULL',
        'hours_worked': 'REAL NOT NULL',
        'FOREIGN KEY(employee_id)': 'REFERENCES employees(id)'
    })

    inventory.create_table('expenses', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'type_id': 'INTEGER NOT NULL',
        'amount': 'REAL NOT NULL',
        'date': 'TEXT NOT NULL'
    })

    inventory.create_table('expense_types', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'description': 'TEXT'
    })   



