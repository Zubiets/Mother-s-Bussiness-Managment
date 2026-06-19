import sqlite3

# model to manipulate easier the database 
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
     
    def select_all(self, table_name):
        query = f"SELECT * FROM {table_name}"
        return self.execute_query(query)
        
    def insert_item(self, table_name, item_data):
        columns = ", ".join(item_data.keys())
        placeholders = ", ".join(["?" for _ in item_data])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.execute_query(query, tuple(item_data.values()))
    
    def update_item(self, table_name, item_id, update_data):
        set_str = ", ".join([f"{col} = ?" for col in update_data.keys()])
        query = f"UPDATE {table_name} SET {set_str} WHERE id = ?"
        self.execute_query(query, tuple(update_data.values()) + (item_id,))

# Create an instance of the Database class and connect to the database
inventory = Database('data/inventory.db')
inventory.connect()

# create the tables using the database model
def create_tables():
    inventory.create_table('categories', {  # different important parts from the local
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
        'price': 'REAL NOT NULL',
        'qr_code': 'TEXT NOT NULL',
        'FOREIGN KEY(category_id)': 'REFERENCES categories(id)'
    })

    inventory.create_table('sales', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'discount': 'REAL NOT NULL DEFAULT 0',
        'total_price': 'REAL NOT NULL',
        'date': 'DATE NOT NULL',
        'time': 'TIME NOT NULL'
    })

    inventory.create_table('sale_details', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'sale_id': 'INTEGER NOT NULL',
        'product_id': 'INTEGER NOT NULL',
        'quantity': 'INTEGER NOT NULL',
        'price': 'REAL NOT NULL',
        'FOREIGN KEY(sale_id)': 'REFERENCES sales(id)',
        'FOREIGN KEY(product_id)': 'REFERENCES products(id)'
    })

    inventory.create_table('users', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'username': 'TEXT NOT NULL',
        'password': 'TEXT NOT NULL'
    })

    inventory.create_table('employees', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'salary': 'REAL NOT NULL',
        'contact_info': 'TEXT NOT NULL'
    })

    inventory.create_table('time_working', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'employee_name': 'INTEGER NOT NULL',
        'date': 'DATE NOT NULL',
        'time_in': 'TIME NOT NULL',
        'time_out': 'TIME NOT NULL',
        'day_payment': 'REAL NOT NULL',
        'extra': 'REAL NOT NULL DEFAULT 0',
        'FOREIGN KEY(employee_id)': 'REFERENCES employees(id)'
    })

    inventory.create_table('expenses', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'category_id': 'INTEGER NOT NULL',
        'amount': 'REAL NOT NULL',
        'date': 'DATE NOT NULL',
        'time': 'TIME NOT NULL',
        'FOREIGN KEY(category_id)': 'REFERENCES categories(id)'
    })

    inventory.execute_query("UNIQUE INDEX IF NOT EXISTS idx_product_name ON products(name)")
    inventory.execute_query("UNIQUE INDEX IF NOT EXISTS idx_user_username ON users(username)")
    inventory.execute_query("UNIQUE INDEX IF NOT EXISTS idx_supplier_name ON suppliers(name)")
    inventory.execute_query("UNIQUE INDEX IF NOT EXISTS idx_category_name ON categories(name)")
    inventory.execute_query("UNIQUE INDEX IF NOT EXISTS idx_employee_name ON employees(name)")
    inventory.execute_query("UNIQUE INDEX IF NOT EXISTS idx_user_username ON users(username)")





