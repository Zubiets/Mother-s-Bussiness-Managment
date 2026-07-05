from . import database
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import dateutil


db: database.Database = None
class Crud:
    MAIN_TABLE = None

    def _init_(self, id: int):
        self.id = id

    @classmethod
    def search_by_parameter(cls, parameter: str, value):
        result = db.execute_query(f"SELECT * FROM {cls.MAIN_TABLE} WHERE {parameter} = ?", (value, ))
        if len(result) == 1:
            return cls(*result[0])
        return result
    
    def add(self):
        return db.insert_item(f'{self.MAIN_TABLE}', dict(list(vars(self).items())[1:]))


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
            return cls(*result[0])
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
    def __init__(self, id: int, name: str, category_id: int, price: int, amount: int = 1, state = "ACTIVE", qr_code = None, category = ""):
        super()._init_(id)
        self.name = name
        self.categories_id = category_id
        self.price = price
        self.amount = amount
        self.state = state
        self.qr_code = qr_code
        self.category = category
        if amount == 0:
            self.state = "INACTIVE"
    
class Category(Crud_two_tables):
    MAIN_TABLE = 'categories'
    SECONDARY_TABLE = 'suppliers'
    def __init__(self, id: int, name: str, supplier_id: int, state: str = "ACTIVE", description = "", supplier = ""):
        super()._init_(id)
        self.name = name 
        self.suppliers_id = supplier_id
        self.state = state
        self.description = description
        self.supplier = supplier

class Supplier(Crud):
    MAIN_TABLE = "suppliers"
    def __init__(self, id: int, name, contact_info, state = "ACTIVE"):
        super()._init_(id)
        self.name = name
        self.contact_info = contact_info
        self.state = state
class Sale(Crud):
    MAIN_TABLE = "sales"
    def __init__(self, id: int, datetime: str, total_price = 0.0, discount = 0):
        super()._init_(id)
        self.datetime = datetime
        self.total_price = total_price
        self.discount = discount

    def add_sale_detail(self, product_id: int, quantity: int, price: int):
        db.execute_query("INSERT INTO sale_details (sale_id, product_id, quantity) VALUES (?, ?, ?)", 
                                        (self.id, product_id, quantity))
        self.total_price += price * quantity

    def get_sale_details(self):
        return db.execute_query("""SELECT products.name, quantity, products.price FROM sale_details
                                                JOIN products ON sale_details.product_id = products.id
                                                WHERE sale_id = ?""", (self.id,))

    def update_sale_detail(self, product_id: int, quantity: int, price: int):
        db.execute_query("UPDATE sale_details SET quantity = ? WHERE sale_id = ? AND product_id = ?", 
                                        (quantity, self.id, product_id))
        self.total_price += price * quantity

    def close_sale(self):
        self.total_price = self.total_price * self.discount

class Employee(Crud):
    MAIN_TABLE = 'employees'
    def __init__(self, id: int, name: str, salary: int, contact: str, state = "ACTIVE"):
        super()._init_(id)
        self.name = name
        self.salary = salary
        self.contact_info = contact
        self.state = state

class Work_day(Crud_two_tables):
    MAIN_TABLE = "time_worked"
    SECONDARY_TABLE = "employees"
    second_parameter = "salary"

    def __init__(self, id, employee_id, date: str, time_in: str, 
                 time_out = "00/00/00 00:00:00", payment = 0,state = "UNPAID", extra = 0, employee_salary = 0):
        self.id = id
        self.employee_id = employee_id
        self.date = date
        self.time_in = time_in
        self.time_out = time_out
        self.payment = payment
        self.state = state
        self.extra = extra
        self.employee_salary = employee_salary

    @staticmethod
    def search_by_parameter(employee_id, date):
        result = db.execute_query(f"""SELECT {Work_day.MAIN_TABLE}.*, {Work_day.SECONDARY_TABLE}.{Work_day.second_parameter}
                                            FROM {Work_day.MAIN_TABLE}
                                            JOIN {Work_day.SECONDARY_TABLE} ON {Work_day.MAIN_TABLE}.employee_id = {Work_day.SECONDARY_TABLE}.id
                                            WHERE {Work_day.MAIN_TABLE}.employee_id = ? AND {Work_day.MAIN_TABLE}.date = ?""", (employee_id, date))
        if len(result) == 1:
            return Work_day(*result[0])
        elif len(result) > 1:
            return [Product(*fila) for fila in result]
        return result
    
    def day_over(self, extra, time_out: str):
        self.time_out = time_out
        self.extra = extra
        time_in = datetime.datetime.strptime(self.time_in, "%Y/%m/%d %H:%M:%S")
        time_out = datetime.datetime.strptime(self.time_out, "%Y/%m/%d %H:%M:%S")
        self.payment = (self.employee_salary * ((time_out - time_in).total_seconds()/3600)) + self.extra
        self.update()

class Expense(Crud_two_tables):
    MAIN_TABLE = 'expenses'
    SECONDARY_TABLE = 'categories'
    def __init__(self, id: int, name: str, category_id, amount: float, datetime: str, category: str = ""):
        super()._init_(id)
        self.name = name
        self.categories_id = category_id
        self.amount = amount
        self.datetime = datetime
        self.category = category
    
class Loan(Crud_two_tables):
    MAIN_TABLE = 'loans'
    SECONDARY_TABLE = 'suppliers'
    def __init__(self, id: int, supplier_id, amount: float, date: str, installments: int, state = "ACTIVE", supplier = ''):
        super()._init_(id)
        self.suppliers_id = supplier_id
        self.amount = amount
        self.date = date
        self.installments = installments
        self.state = state
        self.supplier = supplier

    def determine_payments_dates(self, time_intervals: str):
        loan_date = datetime.datetime.strptime(self.date, "%Y-%m-%d")
        for i in range(self.installments):
            if time_intervals == "WEEKLY":
                payment_date = loan_date + datetime.timedelta(weeks=i)
            elif time_intervals == "BIWEEKLY":
                payment_date = loan_date + datetime.timedelta(weeks=2*i)
            elif time_intervals == "MONTHLY":
                payment_date = dateutil.relativedelta.relativedelta(months=i)
                payment_date = loan_date + payment_date
            db.execute_query("INSERT INTO installments_details (loans_id, number, date) VALUES (?, ?, ?)", (self.id, i+1, payment_date.strftime("%Y-%m-%d")))

    def update_installment_state(self, id, state):
        db.execute_query("UPDATE installments_details SET state = ? WHERE id = ?", (state, id))


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
