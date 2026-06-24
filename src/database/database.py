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
    
    def insert_item(self, table_name, item_data):
        columns = ", ".join(item_data.keys())
        placeholders = ", ".join(["?" for _ in item_data])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.execute_query(query, tuple(item_data.values()))
    
    def update_item(self, table_name, item_id, update_data):
        set_str = ", ".join([f"{col} = ?" for col in update_data.keys()])
        query = f"UPDATE {table_name} SET {set_str} WHERE id = ?"
        self.execute_query(query, tuple(update_data.values()) + (item_id,))
     
    def fetch_all(self, table_name):
        query = f"SELECT * FROM {table_name}"
        return self.execute_query(query)

    def fetch_one(self, table_name, item):
        return self.execute_query(f"SELECT {item} FROM {table_name}")
        


# create the tables using the database model
def create_tables(db):
    db.create_table('categories', {  # different important parts from the local
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'suppliers_id': 'INTEGER NOT NULL',
        'description': 'TEXT',
        'FOREIGN KEY(suppliers_id)': 'REFERENCES suppliers(id)'
    })

    db.create_table('suppliers', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'contact_info': 'TEXT NOT NULL'
    })

    db.create_table('products', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'categories_id': 'INTEGER NOT NULL',
        'price': 'REAL NOT NULL',
        'state': "TEXT NOT NULL DEFAULT 'ACTIVE'",
        'qr_code': 'TEXT',
        'FOREIGN KEY(categories_id)': 'REFERENCES categories(id)'
    })

    db.create_table('sales', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'datetime': 'DATE NOT NULL',
        'total_price': 'REAL NOT NULL',
        'discount': 'REAL NOT NULL DEFAULT 0'
    })

    db.create_table('sale_details', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'sale_id': 'INTEGER NOT NULL',
        'product_id': 'INTEGER NOT NULL',
        'quantity': 'INTEGER NOT NULL',
        'price': 'REAL NOT NULL',
        'FOREIGN KEY(sale_id)': 'REFERENCES sales(id)',
        'FOREIGN KEY(product_id)': 'REFERENCES products(id)'
    })

    db.create_table('users', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'username': 'TEXT NOT NULL',
        'password': 'TEXT NOT NULL'
    })

    db.create_table('employees', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'salary': 'REAL NOT NULL',
        'contact_info': 'TEXT NOT NULL'
    })

    db.create_table('time_working', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'employee_id': 'INTEGER NOT NULL',
        'date': 'DATE NOT NULL',
        'time_in': 'TIME NOT NULL',
        'time_out': 'TIME NOT NULL',
        'payment': 'REAL NOT NULL',
        'extra': 'REAL NOT NULL DEFAULT 0',
        'FOREIGN KEY(employee_id)': 'REFERENCES employees(id)'
    })

    db.create_table('expenses', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'categories_id': 'INTEGER NOT NULL',
        'amount': 'REAL NOT NULL',
        'date': 'DATE NOT NULL',
        'time': 'TIME NOT NULL',
        'FOREIGN KEY(categories_id)': 'REFERENCES categories(id)'
    })

    db.create_table('loans', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'suppliers_id': 'INTEGER NOT NULL',
        'amount': 'INTEGER NOT NULL',
        'loan_date': 'DATE NOT NULL',
        'installments': 'INTEGER NOT NULL',
        'FOREIGN KEY(suppliers_id)': 'REFERENCES supplier(id)'
    })

    db.create_table('installments_dates', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'loan_id': 'INTEGER NOT NULL',
        'number': 'INTEGER NOT NULL',
        'date': 'DATE NOT NULL',
        'state': "TEXT NOT NULL DEFAULT 'UNPAID'",
        'FOREIGN KEY(loan_id)': 'REFERENCES loans(id)'
    })

    db.execute_query("CREATE UNIQUE INDEX IF NOT EXISTS idx_product_name ON products(name)")
    db.execute_query("CREATE UNIQUE INDEX IF NOT EXISTS idx_product_code ON products(qr_code)")
    db.execute_query("CREATE UNIQUE INDEX IF NOT EXISTS idx_user_username ON users(username)")
    db.execute_query("CREATE UNIQUE INDEX IF NOT EXISTS idx_category_name ON categories(name)")
    db.execute_query("CREATE UNIQUE INDEX IF NOT EXISTS idx_supplier_name ON suppliers(name)")
    db.execute_query("CREATE UNIQUE INDEX IF NOT EXISTS idx_employee_name ON employees(name)")

# App's predetermine database connection and tables creation
def predet_connection(db: Database):
    db.connect()
    create_tables(db)


