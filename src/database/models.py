import database
from werkzeug.security import check_password_hash, generate_password_hash
class Product:
    def __init__(self, id, name, category, price, category_description = ""):
        self.id = id
        self.name = name
        self.category = category
        self.price = price
    


class Category:
    def __init__(self, id, name, supplier, description = ""):
        self.id = id
        self.name = name
        self.supplier = supplier
        self.description = description

class Supplier:
    def __init__(self, name, contact_info):
        self.name = name
        self.contact_info = contact_info

    def add_supplier(self):
        try:
            database.inventory.execute_query("INSERT INTO suppliers (name, contact_info) VALUES (?, ?)", 
                                            (self.name, self.contact_info))
        except Exception as e:
            print(f"Error adding supplier: {e}")
    
    def update_supplier(self):
        try:
            database.inventory.execute_query("UPDATE suppliers SET contact_info = ? WHERE name = ?", 
                                            (self.contact_info, self.name))
        except Exception as e:
            print(f"Error updating supplier: {e}")

    def delete_supplier(self):
        try:
            database.inventory.execute_query("DELETE FROM suppliers WHERE name = ?", (self.name,))
        except Exception as e:
            print(f"Error deleting supplier: {e}")
    
    
class Sale:
    def __init__(self, date, time, discount = 0):
        self.total_price = 0
        self.date = date
        self.time = time
        self.discount = discount

    def add_sale(self):
        try:
            database.inventory.execute_query("INSERT INTO sales (total_price, date, time, discount) VALUES (?, ?, ?, ?)", 
                                            (self.total_price, self.date, self.time, self.discount))
        except Exception as e:
            print(f"Error adding sale: {e}")

    def add_sale_detail(self, product, quantity, price):
        try:
            sale_id = database.inventory.execute_query("SELECT id FROM sales WHERE date = ? AND time = ?", (self.date, self.time))[0][0]
            product_id = database.inventory.execute_query("SELECT id FROM products WHERE name = ?", (product))[0][0]
            database.inventory.execute_query("INSERT INTO sale_details (sale_id, product_id, quantity, price) VALUES (?, ?, ?, ?)", 
                                            (sale_id, product_id, quantity, price))
            self.total_price += price * quantity     
        except Exception as e:
            print(f"Error adding sale detail: {e}")
    
    def calculate_total_price(self):
        try:
            self.total_price = self.total_price * (1 - self.discount/100)
            database.inventory.execute_query("UPDATE sales SET total_price = ? WHERE date = ? AND time = ?", 
                                            (self.total_price, self.date, self.time))
        except Exception as e:
            print(f"Error calculating total price: {e}")
    
    def delete_sale(self):
        try:
            sale_id = database.inventory.execute_query("SELECT id FROM sales WHERE date = ? AND time = ?", (self.date, self.time))[0][0]
            database.inventory.execute_query("DELETE FROM sale_details WHERE sale_id = ?", (sale_id,))
            database.inventory.execute_query("DELETE FROM sales WHERE id = ?", (sale_id,))
        except Exception as e:
            print(f"Error deleting sale: {e}")

    def get_sale_details(self):
        try:
            sale_id = database.inventory.execute_query("SELECT id FROM sales WHERE date = ? AND time = ?", (self.date, self.time))[0][0]
            details = database.inventory.execute_query("SELECT product_id, quantity, price FROM sale_details WHERE sale_id = ?", (sale_id,))
            return details
        except Exception as e:
            print(f"Error getting sale details: {e}")
            return []
        
class Employee:
    def __init__(self, id, name, salary, contact):
        self.id = id
        self.name = name
        self.salary = salary
        self.contact = contact
    
    def add_employee(self):
        try:
            database.inventory.execute_query("INSERT INTO employees (name, salary, contact_info) VALUES (?, ?, ?)", 
                                            (self.name, self.salary, self.contact))
        except Exception as e:
            print(f"Error adding employee: {e}")
    
    def delete_employee(self):
        try:
            database.inventory.execute_query("DELETE FROM employees WHERE name = ?", (self.name,))
        except Exception as e:
            print(f"Error deleting employee: {e}")

    def update_employee(self):
        try:
            database.inventory.execute_query("UPDATE employees SET salary = ?, contact_info = ? WHERE name = ?", 
                                            (self.salary, self.contact, self.name))
        except Exception as e:
            print(f"Error updating employee: {e}")

    def registrer_enter_time(self, date, time_in):
        try:
            database.inventory.execute_query("INSERT INTO time_working (employee_name, date, time_in) VALUES (?, ?, ?)", 
                                            (self.name, date, time_in))
        except Exception as e:
            print(f"Error registering enter time: {e}")

    def registrer_exit_time(self, date, time_out, extra):
        try:
            database.inventory.execute_query("UPDATE time_working SET time_out = ?, day_payment = ?, extra = ? WHERE employee_name = ? AND date = ?", 
                                            (time_out, self.name, date, extra))
        except Exception as e:
            print(f"Error registering exit time: {e}")

    def day_payment(self, date):
        try:
            payment = database.inventory.execute_query("SELECT day_payment FROM time_working WHERE employee_name = ? AND date = ?", 
                                            (self.name, date))[0][0]
            return payment
        except Exception as e:
            print(f"Error getting day payment: {e}")
            return 0

class Expense:
    def __init__(self, name, amount, date, time, category):
        self.name = name
        self.amount = amount
        self.date = date
        self.time = time
        self.category = category
    
    
    
class User:
    def __init__(self,username, password):
        self.username = username
        self.password = password
    
    def check_password(self):
        try:
            return check_password_hash(
                database.inventory.execute_query("SELECT password FROM users WHERE name = ?", (self.username,))
                                                , self.password)
        except Exception as e:
            print(f"Error checking password: {e}")
            return False

    def set_user(self):
        try: 
            database.inventory.execute_query("INSERT INTO users (name, password) VALUES (?, ?)", 
                                            (self.username, generate_password_hash(self.password)))
        except Exception as e:
            print(f"Error setting user: {e}")

    def update_password(self):
        try:
            database.inventory.execute_query("UPDATE users SET password = ? WHERE name = ?", 
                                             (generate_password_hash(self.password), self.username))
        except Exception as e:
            print(f"Error updating password: {e}")
    
    def delete_user(self):
        try:
            database.inventory.execute_query("DELETE FROM users WHERE name = ?", (self.username,))
        except Exception as e:
            print(f"Error deleting user: {e}")