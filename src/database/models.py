from . import database
from werkzeug.security import check_password_hash, generate_password_hash


db: database.Database = None
class Crud:
    MAIN_TABLE = None

    def _init_(self, id: int):
        self.id = id

    @classmethod
    def search_by_parameter(cls, parameter: str, value):
        result = db.execute_query(f"SELECT * FROM {cls.MAIN_TABLE} WHERE {parameter} = ?", (value, ))
        if result:
            return result[0]
        return None
    
    def add(self):
        db.insert_item(f'{self.MAIN_TABLE}', dict(list(vars(self).items())[1:]))

    def delete(self):
        db.execute_query(f"DELETE FROM {self.MAIN_TABLE} WHERE id = ?", (self.id,))

    def update(self):
        db.update_item(f'{self.MAIN_TABLE}', self.id, dict(list(vars(self).items())[1:]))

class Crud_two_tables:
    MAIN_TABLE = None
    SECONDARY_TABLE = None

    def _init_(self, id: int):
        self.id = id

    @classmethod
    def search_by_parameter(cls, parameter: str, value):
        result = db.execute_query(f"""SELECT {cls.MAIN_TABLE}.*, {cls.SECONDARY_TABLE}.name
                                                FROM {cls.MAIN_TABLE}
                                                JOIN {cls.SECONDARY_TABLE} ON {cls.MAIN_TABLE}.{cls.SECONDARY_TABLE}_id = {cls.SECONDARY_TABLE}.id
                                                WHERE {cls.MAIN_TABLE}.{parameter} = ?""", (value, ))
        if result:
            return result[0]
        return None

    def add(self):
        db.insert_item(f'{self.MAIN_TABLE}', dict(list(vars(self).items())[1:-1]))
    
    def delete(self):
        db.execute_query(f"DELETE FROM {self.MAIN_TABLE} WHERE id = ?", (self.id,) )
        
    def update(self):
        db.update_item(f'{self.MAIN_TABLE}', self.id, dict(list(vars(self).items())[1:-1]))

class Product(Crud_two_tables):
    MAIN_TABLE = 'products'
    SECONDARY_TABLE = 'categories'
    def __init__(self, id: int, name: str, category_id, price: int, state = "ACTIVE", qr_code = None, category = ""):
        super()._init_(id)
        self.name = name
        self.categories_id = category_id
        self.price = price
        self.state = state
        self.qr_code = qr_code
        self.category = category
    
class Category(Crud_two_tables):
    MAIN_TABLE = 'categories'
    SECONDARY_TABLE = 'suppliers'
    def __init__(self, id: int, name: str, supplier_id, description = "", supplier = ""):
        super()._init_(id)
        self.name = name 
        self.suppliers_id = supplier_id
        self.description = description
        self.supplier = supplier

class Supplier(Crud):
    MAIN_TABLE = "suppliers"
    def __init__(self, id: int, name, contact_info):
        super()._init_(id)
        self.name = name
        self.contact_info = contact_info

class Sale(Crud):
    MAIN_TABLE = "sales"
    def __init__(self, id: int, datetime, total_price = 0, discount = 0.0):
        super()._init_(id)
        self.datetime = datetime
        self.total_price = total_price
        self.discount = discount

    def add_sale(self):
        db.execute_query("INSERT INTO sales (total_price, datetime, discount) VALUES (?, ?, ?, ?)", 
                                        (self.total_price, self.datetime, self.discount))

    def add_sale_detail(self, id: int, product, quantity, price):
        product_id = Product.search_by_name((product)[0][0])[0]
        db.execute_query("INSERT INTO sale_details (sale_id, product_id, quantity, price) VALUES (?, ?, ?, ?)", 
                                        (self.id, product_id, quantity, price))
        self.total_price += price * quantity
    
    def calculate_total_price(self):
        self.total_price = self.total_price * (1 - self.discount/100)
        db.execute_query("UPDATE sales SET total_price = ? WHERE date = ? AND time = ?", 
                                        (self.total_price, self.datetime))
    
    def delete_sale(self):
        db.execute_query("DELETE FROM sale_details WHERE sale_id = ?", (self.id,))
        db.execute_query("DELETE FROM sales WHERE id = ?", (self.id,))

    def get_sales_details(self):
        return db.execute_query("""SELECT product.name, quantity, price FROM sale_details
                                                JOIN products ON sale_details.product_id = products.id
                                                WHERE sale_id = ?""", (self.id,))

class Employee(Crud):
    MAIN_TABLE = 'employees'
    def __init__(self, id: int, name: str, salary: int, contact: str):
        super()._init_(id)
        self.name = name
        self.salary = salary
        self.contact_info = contact

    def registrer_enter_time(self, date, time_in):
        db.execute_query("INSERT INTO time_working (employee_id, employee_name, date, time_in) VALUES (?, ?, ?)", 
                                        (self.id, self.name, date, time_in))

    def registrer_exit_time(self, date, time_out, extra = 0.0):
        db.execute_query("UPDATE time_working SET time_out = ?, payment = ?, extra = ? WHERE employee_name = ? AND date = ?", 
                                        (time_out, self.name, date, extra))

class Expense(Crud_two_tables):
    MAIN_TABLE = 'expenses'
    SECONDARY_TABLE = 'categories'
    def __init__(self, id: int, name: int, category_id, amount: int, datetime, category: str):
        super()._init_(id)
        self.name = name
        self.categories_id = category_id
        self.amount = amount
        self.datetime = datetime
        self.category = category
    
class Loan(Crud_two_tables):
    MAIN_TABLE = 'loans'
    SECONDARY_TABLE = 'suppliers'
    def __init__(self, id: int, supplier_id, amount: int, loan_date: str, installments: int, supplier = ''):
        super()._init_(id)
        self.suppliers_id = supplier_id
        self.amount = amount
        self.loan_date = loan_date
        self.installments = installments
        self.supplier = supplier

    def determine_payments_dates(self, id: int, time_intervals: str):
        pass
class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
    
    def check_password(self):
        return check_password_hash(
            db.execute_query("SELECT password FROM users WHERE name = ?", (self.username,))
                                            , self.password)

    def set_user(self):
        db.execute_query("INSERT INTO users (name, password) VALUES (?, ?)", 
                                        (self.username, generate_password_hash(self.password)))

    def update_password(self):
        db.execute_query("UPDATE users SET password = ? WHERE name = ?", generate_password_hash(self.password), self.username)
    
    def delete_user(self):
        db.execute_query("DELETE FROM users WHERE name = ?", (self.username,))
