import database

class Product:
    def __init__(self, id, name, category, price, category_description = ""):
        self.id = id
        self.name = name
        self.category = category
        self.price = price
    

class category:
    def __init__(self, id, name, supplier, description = ""):
        self.id = id
        self.name = name
        self.supplier = supplier
        self.description = description

class Supplier:
    def __init__(self, id, name, contact_info):
        self.id = id
        self.name = name
        self.contact_info = contact_info
    
class Sale:
    def __init__(self, id, total_price, date, time):
        self.id = id
        self.total_price = total_price
        self.date = date
        self.time = time
    

class Employee:
    def __init__(self, id, name, salary, phone = ""):
        self.id = id
        self.name = name
        self.salary = salary
        self.phone = phone
    
class Expense:
    def __init__(self, id, name, amount, date, time, category):
        self.id = id
        self.name = name
        self.amount = amount
        self.date = date
        self.time = time

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password