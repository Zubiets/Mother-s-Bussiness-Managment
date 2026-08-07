import sqlite3
from typing import List

# model to manipulate easier the database 
class Database:
    def __init__(self, db_path: str):
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

    def execute_query(self, query, params: tuple = None):
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
        
    def create_table(self, table_name, columns: dict):
        columns_str = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
        self.execute_query(query)
    
    def insert_item(self, table_name, item_data: dict):
        columns = ", ".join(item_data.keys())
        placeholders = ", ".join(["?" for _ in item_data])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.execute_query(query, tuple(item_data.values()))
    
    def update_item(self, table_name, item_id, update_data: dict):
        set_str = ", ".join([f"{col} = ?" for col in update_data.keys()])
        query = f"UPDATE {table_name} SET {set_str} WHERE id = ?"
        self.execute_query(query, tuple(update_data.values()) + (item_id,))

    def fetch_table(self, table_name: str, secondary: str = None, columns: List = None):    
        cursor = self.connection.cursor()

        if not columns:
            return cursor.execute(f"SELECT * FROM {table_name}")

        if not secondary:
            columns = ", ".join(columns)
            cursor.execute(f"SELECT {columns} FROM {table_name}")
        else:
            for i, column in enumerate(columns[:-1]):
                columns[i] = f"{table_name}.".join(column)
            columns[-1] = f"{secondary}.name"
            columns = ", ".join(columns)

            cursor.execute(f"""SELECT {columns} FROM {table_name}
                                JOIN {secondary} ON {table_name}.{secondary}_id = {secondary}.id""")
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
        


        


# create the tables using the database model
def create_tables(db):
    db.create_table('categories', {  # different important parts from the local
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'suppliers_id': 'INTEGER NOT NULL',
        'name': 'TEXT NOT NULL',
        'state': "TEXT NOT NULL DEFAULT 'ACTIVE'",
        'FOREIGN KEY(suppliers_id)': 'REFERENCES suppliers(id)'
    })

    db.create_table('suppliers', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'contact_info': 'TEXT NOT NULL',
        'state': "TEXT NOT NULL DEFAULT 'ACTIVE'",
    })

    db.create_table('products', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'categories_id': 'INTEGER NOT NULL',
        'name': 'TEXT NOT NULL',
        'price': 'REAL NOT NULL',
        "amount": "INTEGER NOT NULL DEFAULT 1",   # if the product is active, there's at least one sample
        'state': "TEXT NOT NULL DEFAULT 'ACTIVE'",
        'qr_code': 'TEXT',
        'FOREIGN KEY(categories_id)': 'REFERENCES categories(id)'
    })

    db.create_table('sales', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'datetime': 'DATE NOT NULL',
        'total_price': 'REAL NOT NULL',
        "payment": 'REAL NOT NULL',
        "payment_method": "REAL NOT NULL DEFAULT 'Efectivo'",
        'discount': 'REAL NOT NULL DEFAULT 0'
    })

    db.create_table('sale_details', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'sale_id': 'INTEGER NOT NULL',
        'product_id': 'INTEGER NOT NULL',
        'quantity': 'INTEGER NOT NULL',
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
        'contact_info': 'TEXT NOT NULL',
        'state': "TEXT NOT NULL DEFAULT 'ACTIVE'",
    })

    db.create_table('time_worked', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'employee_id': 'INTEGER NOT NULL',
        'date': 'DATE NOT NULL',
        'time_in': 'DATE NOT NULL',
        'time_out': "DATE NOT NULL",
        'payment': 'REAL NOT NULL DEFAULT 0',
        'state': "TEXT NOT NULL DEFAULT 'UNPAID'",
        'extra': 'REAL NOT NULL DEFAULT 0',
        'FOREIGN KEY(employee_id)': 'REFERENCES employees(id)'
    })

    db.create_table('expenses', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'categories_id': 'INTEGER NOT NULL',
        'name': 'TEXT NOT NULL',
        'amount': 'REAL NOT NULL',
        "payment_method": "REAL NOT NULL DEFAULT 'Efectivo'",
        'datetime': 'DATE NOT NULL',
        'FOREIGN KEY(categories_id)': 'REFERENCES categories(id)'
    })

    db.create_table('loans', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'suppliers_id': 'INTEGER NOT NULL',
        'amount': 'REAL NOT NULL',
        'date': 'DATE NOT NULL',
        'installments': 'INTEGER NOT NULL',
        'state': "TEXT NOT NULL DEFAULT 'ACTIVE'",
        'FOREIGN KEY(suppliers_id)': 'REFERENCES supplier(id)'
    })

    db.create_table('installments_details', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'loans_id': 'INTEGER NOT NULL',
        'number': 'INTEGER NOT NULL',
        'date': 'DATE NOT NULL',
        "payment_method": "REAL NOT NULL DEFAULT 'Efectivo'",
        'state': "TEXT NOT NULL DEFAULT 'UNPAID'",
        'FOREIGN KEY(loans_id)': 'REFERENCES loans(id)'
    })

    db.create_table("tasks", {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'datetime': 'DATE NOT NULL',
        'description': 'TEXT NOT NULL',
        'state': "TEXT NOT NULL DEFAULT 'PENDING'",
        'highlight': "TEXT NOT NULL DEFAULT 'DEACTIVE'"
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
    


