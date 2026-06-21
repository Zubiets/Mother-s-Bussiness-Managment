from . import database
from werkzeug.security import check_password_hash, generate_password_hash

class Crud:
    MAIN_TABLE = None
    SECONDARY_TABLE = None

    @classmethod
    def search_by_parameter(cls, parameter: str, value):
        return database.inventory.execute_query(f"""SELECT {cls.MAIN_TABLE}.*, {cls.SECONDARY_TABLE}.name
                                                FROM {cls.MAIN_TABLE}
                                                JOIN {cls.SECONDARY_TABLE} ON {cls.MAIN_TABLE}.category_id = {cls.SECONDARY_TABLE}.id
                                                WHERE {cls.MAIN_TABLE}.{parameter} = ?""", (value, ))

    def add(self):
        database.inventory.insert_item(f'{self.MAIN_TABLE}', dict(list(vars(self).items())[1:-1]))
    
    def delete(self):
        database.inventory.execute_query(f"DELETE FROM {self.MAIN_TABLE} WHERE id = ?", self.id)
        
    def update(self):
        database.inventory.update_item(f'{self.MAIN_TABLE}', self.id, dict(list(vars(self).items())[1:-1]))
class Product(Crud):
    MAIN_TABLE = 'products'
    SECONDARY_TABLE = 'categories'
    def __init__(self, id: int, name: str, category_id: int, price: int, state = "ACTIVE", qr_code = None, category = ""):
        self.id = id
        self.name = name
        self.category_id = category_id
        self.price = price
        self.state = state
        self.qr_code = qr_code
        self.category = category
    
class Category(Crud):
    MAIN_TABLE = 'categories'
    SECONDARY_TABLE = 'suppliers'
    def __init__(self, id: int, name: str, supplier_id: int, description = "", supplier = ""):
        self.id = id
        self.name = name
        self.supplier_id = supplier_id
        self.description = description
        self.supplier = supplier

class Supplier(Crud):
    MAIN_TABLE = "suppliers"
    def __init__(self, id,  name, contact_info):
        self.id = id
        self.name = name
        self.contact_info = contact_info
    
    @classmethod
    def search_by_parameter(cls, parameter: str, value):
        return database.inventory.execute_query(f"SELECT * FROM {cls.MAIN_TABLE} WHERE {parameter} = ?", (value, ))[0]

    def add(self):
        database.inventory.insert_item(f'{self.MAIN_TABLE}', dict(list(vars(self).items())[1:]))

    def update(self):
        database.inventory.update_item(f'{self.MAIN_TABLE}', self.id, dict(list(vars(self).items())[1:]))

class Sale:
    def __init__(self, id: int, date: str, time: str, discount = 0.0):
        self.id = id
        self.total_price = 0
        self.date = date
        self.time = time
        self.discount = discount

    def add_sale(self):
        database.inventory.execute_query("INSERT INTO sales (total_price, date, time, discount) VALUES (?, ?, ?, ?)", 
                                        (self.total_price, self.date, self.time, self.discount))

    def add_sale_detail(self, product, quantity, price):
        product_id = Product.search_by_name((product)[0][0])[0]
        database.inventory.execute_query("INSERT INTO sale_details (sale_id, product_id, quantity, price) VALUES (?, ?, ?, ?)", 
                                        (self.id, product_id, quantity, price))
        self.total_price += price * quantity
    
    def calculate_total_price(self):
        self.total_price = self.total_price * (1 - self.discount/100)
        database.inventory.execute_query("UPDATE sales SET total_price = ? WHERE date = ? AND time = ?", 
                                        (self.total_price, self.date, self.time))
    
    def delete_sale(self):
        database.inventory.execute_query("DELETE FROM sale_details WHERE sale_id = ?", (self.id,))
        database.inventory.execute_query("DELETE FROM sales WHERE id = ?", (self.id,))

    def get_sales_details(self):
        return database.inventory.execute_query("""SELECT product.name, quantity, price FROM sale_details
                                                JOIN products ON sale_details.product_id = products.id
                                                WHERE sale_id = ?""", (self.id,))


class Employee(Crud):
    MAIN_TABLE = 'employees'
    def __init__(self, id: int, name: str, salary: int, contact: str):
        self.id = id
        self.name = name
        self.salary = salary
        self.contact = contact

    def search_by_parameter(parameter: str, value):
        return database.inventory.execute_query(f"SELECT * FROM suppliers WHERE {parameter} = ?", (value,))
    
    def add(self):
        database.inventory.insert_item(f'{self.MAIN_TABLE}', dict(list(vars(self).items())))

    def update(self):
        database.inventory.update_item(f'{self.MAIN_TABLE}', self.id, dict(list(vars(self).items())))

    def registrer_enter_time(self, date: str, time_in: str):
        database.inventory.execute_query("INSERT INTO time_working (employee_name, date, time_in) VALUES (?, ?, ?)", 
                                        (self.name, date, time_in))

    def registrer_exit_time(self, date: str, time_out: str, extra = 0.0):
        database.inventory.execute_query("UPDATE time_working SET time_out = ?, payment = ?, extra = ? WHERE employee_name = ? AND date = ?", 
                                        (time_out, self.name, date, extra))

class Expense(Crud):
    MAIN_TABLE = 'expenses'
    SECONDARY_TABLE = 'categories'
    def __init__(self, id: int, name: int, category_id: int, amount: int, date: str, time: str, category: str):
        self.id = id
        self.name = name
        self.category_id = category_id
        self.amount = amount
        self.date = date
        self.time = time
        self.category = category
    
class Loan(Crud):
    MAIN_TABLE = 'loans'
    SECONDARY_TABLE = 'suppliers'
    def __init__(self, id: int, supplier_id: int, amount: int, loan_date: str, installments: int, supplier = ''):
        self.id = id
        self.supplier_id = supplier_id
        self.amount = amount
        self.loan_date = loan_date
        self.installments = installments
        self.supplier = supplier

    def determine_payments_dates(self, time_intervals: str):
        pass
class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
    
    def check_password(self):
        return check_password_hash(
            database.inventory.execute_query("SELECT password FROM users WHERE name = ?", (self.username,))
                                            , self.password)

    def set_user(self):
        database.inventory.execute_query("INSERT INTO users (name, password) VALUES (?, ?)", 
                                        (self.username, generate_password_hash(self.password)))

    def update_password(self):
        database.inventory.execute_query("UPDATE users SET password = ? WHERE name = ?", generate_password_hash(self.password), self.username)
    
    def delete_user(self):
        database.inventory.execute_query("DELETE FROM users WHERE name = ?", (self.username,))
