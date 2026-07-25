from src.database import database, models

def seed_database():
    db = database.Database("data/inventory.db")
    database.predet_connection(db)
    models.db = db

    # Suppliers
    suppliers = [
        models.Supplier(id=None, name=f"Supplier {i}", contact_info=f"30012345{i:02d}")
        for i in range(1, 11)
    ]
    for s in suppliers:
        s.add()
    supplier_ids = [models.Supplier.search_by_parameter("name", f"Supplier {i}").id for i in range(1, 11)]

    # Categories
    categories = [
        models.Category(id=None, name=f"Category {i}", supplier_id=supplier_ids[i-1], description=f"Description {i}")
        for i in range(1, 11)
    ]
    for c in categories:
        c.add()
    category_ids = [models.Category.search_by_parameter("name", f"Category {i}").id for i in range(1, 11)]

    # Products
    products = [
        models.Product(id=None, name=f"Product {i}", category_id=category_ids[i-1], price=i*1000, qr_code=f"QR{i:04d}")
        for i in range(1, 11)
    ]
    for p in products:
        p.add()
    product_ids = [models.Product.search_by_parameter("qr_code", f"QR{i:04d}").id for i in range(1, 11)]

    # Sales + SaleDetails
    for i in range(1, 11):
        sale = models.Sale(
            id=None,
            datetime=f"2026/07/{i:02d} 09:00:00",
            total_price=0,
            discount=0,
        )
        sale.add()
        sale.id = db.execute_query("SELECT last_insert_rowid()") [0][0]
        sale.add_sale_detail(product_id=product_ids[i-1], quantity=i, price=i*1000)
        sale.total_price = i * i * 1000
        sale.update()

    # Employees
    employees = [
        models.Employee(id=None, name=f"Employee {i}", salary=i*500000, contact=f"31012345{i:02d}")
        for i in range(1, 11)
    ]
    for employee in employees:
        employee.add()
    employee_ids = [models.Employee.search_by_parameter("name", f"Employee {i}").id for i in range(1, 11)]

    # Time worked
    for i, emp_id in enumerate(employee_ids, 1):
        emp = models.Employee.search_by_parameter("name", f"Employee {i}")
        work_day = models.Work_day(
            id=None,
            employee_id=emp.id,
            date=f"2026/07/{i:02d}",
            time_in=f"2026/07/{i:02d} 08:00:00",
            time_out=f"2026/07/{i:02d} 17:00:00",
            payment=0,
            state="UNPAID",
            extra=0,
            employee_salary=emp.salary,
        )
        work_day.add()

    # Expenses
    expenses = [
        models.Expense(
            id=None,
            name=f"Expense {i}",
            category_id=category_ids[i-1],
            amount=i*10000,
            method="Efectivo",
            datetime=f"2026/07/{i:02d} 09:00:00",
        )
        for i in range(1, 11)
    ]
    for e in expenses:
        e.add()

    # Loans + Installments
    for i in range(1, 11):
        loan = models.Loan(
            id=None,
            supplier_id=supplier_ids[i-1],
            amount=i*100000,
            date=f"2026/07/{i:02d}",
            installments=3,
        )
        loan.add()
        loan.id = db.execute_query("SELECT last_insert_rowid()") [0][0]
        loan.determine_payments_dates("MENSUAL")


    # Tasks
    todos = [
        models.Task(
            id=None,
            name=f"Task {i}",
            datetime=f"2026-07-{i:02d} 09:00:00",
            description=f"Description of task {i}",
        )
        for i in range(1, 11)
    ]
    for t in todos:
        t.add()

    print("Database seeded successfully")
    db.disconnect()

if __name__ == "__main__":
    seed_database()