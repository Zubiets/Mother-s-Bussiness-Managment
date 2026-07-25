import pytest
from src.database import database, models
import datetime

@pytest.fixture
def config():
    clean_db = database.Database(":memory:")
    database.predet_connection(clean_db)
    assert clean_db.connection is not None, "Database connection should be established"
    models.db = clean_db
    yield clean_db
    clean_db.disconnect()

@pytest.fixture
def supplier(config):
    s = models.Supplier(id=None, name="Test Supplier", contact_info="123456789")
    assert s.add() != False, "There's a unique contrait fail"
    return models.Supplier.search_by_parameter("name", "Test Supplier")

@pytest.fixture
def category(supplier):
    c = models.Category(id=None, name="Test Category", supplier_id=supplier.id, description="Test description")
    assert c.add() != False, "There's a unique contrait fail"
    return models.Category.search_by_parameter("name", "Test Category")

@pytest.fixture
def product(category):
    p = models.Product(id=None, name="Test Product", category_id=category.id, price=5000, qr_code="TEST123")
    assert p.add() != False, "There's a unique contrait fail"
    return models.Product.search_by_parameter("name", "Test Product")

@pytest.fixture
def sale(product):
    s = models.Sale(id=None, datetime=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), total_price=0, discount=0)
    assert s.add() != False, "There's a unique contrait fail"
    return models.Sale.search_by_parameter("total_price", 0)

@pytest.fixture
def employee(config):
    e = models.Employee(id=None, name="Test Employee", salary=1500000, contact="3001234567")
    assert e.add() != False, "There's a unique contrait fail"
    return models.Employee.search_by_parameter("name", "Test Employee")

def test_suppliers(supplier):
    assert supplier, "Supplier not found after add"
    assert supplier.name == "Test Supplier", "Supplier name mismatch"
    assert supplier.contact_info == "123456789", "Supplier contact mismatch"
    supplier.contact_info = "987654321"
    supplier.update()
    updated = models.Supplier.search_by_parameter("name", "Test Supplier")
    assert updated.contact_info == "987654321", "Supplier update failed"
    supplier.delete()
    result = models.Supplier.search_by_parameter("name", "Test Supplier")
    assert not result, "Supplier not deleted"

def test_categories(category, supplier):
    assert category, "Category not found after add"
    assert category.name == "Test Category", "Category name mismatch"
    assert category.suppliers_id == supplier.id, "Category supplier mismatch"
    category.description = "Updated description"
    category.update()
    updated = models.Category.search_by_parameter("name", "Test Category")
    assert updated.description == "Updated description", "Category update failed"
    category.delete()
    result = models.Category.search_by_parameter("name", "Test Category")
    assert not result, "Category not deleted"

def test_products(product, category):
    assert product, "Product not found after add"
    assert product.price == 5000, "Product price mismatch"
    assert product.state == "ACTIVE", "Product state mismatch"
    assert product.categories_id == category.id, "Product category mismatch"
    result = models.Product.search_by_parameter("qr_code", "TEST123")
    assert result, "Product not found by qr_code"
    product.price = 7500
    product.update()
    updated = models.Product.search_by_parameter("name", "Test Product")
    assert updated.price == 7500, "Product update failed"
    product.amount = 0
    product.update()
    inactive = models.Product.search_by_parameter("name", "Test Product")
    assert inactive.state == "INACTIVE", "Product should be INACTIVE when amount is 0"
    product.delete()
    result = models.Product.search_by_parameter("name", "Test Product")
    assert not result, "Product not deleted"

def test_sales(sale, product, config):
    assert sale, "Sale not found after add"
    assert sale.total_price == 0, "Sale total price mismatch"
    sale.add_sale_detail(product_id=product.id, quantity=2, price=5000)
    buffer = config.execute_query("""SELECT products.name, sale_details.quantity, products.price FROM sale_details
                                                JOIN products ON sale_details.product_id = products.id
                                                WHERE sale_details.sale_id = 1""")
    details = sale.get_sale_details()
    assert details, "Sale details not found"
    assert len(details) == 1, "Unexpected number of sale details"
    assert details[0][1] == 2, "Sale detail quantity mismatch"
    assert details[0][2] == 5000, "Sale detail price mismatch"
    sale.close_sale()
    sale.update()
    updated = models.Sale.search_by_parameter("total_price", sale.total_price)
    assert updated, "Sale not found after close"
    sale.delete()
    result = models.Sale.search_by_parameter("total_price", sale.total_price)
    assert not result, "Sale not deleted"

def test_employees(employee):
    assert employee, "Employee not found after add"
    assert employee.name == "Test Employee", "Employee name mismatch"
    assert employee.salary == 1500000, "Employee salary mismatch"
    assert employee.state == "ACTIVE", "Employee state mismatch"
    employee.salary = 2000000
    employee.update()
    updated = models.Employee.search_by_parameter("name", "Test Employee")
    assert updated.salary == 2000000, "Employee update failed"
    employee.delete()
    result = models.Employee.search_by_parameter("name", "Test Employee")
    assert not result, "Employee not deleted"

def test_work_day(employee):
    work = models.Work_day(
        None,
        employee.id,
        datetime.datetime.now().strftime("%Y/%m/%d"),
        datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    )
    work.add()
    work = models.Work_day.search_by_parameter(employee.id, work.date)
    assert work, "Work day not found after add"
    assert work.id == 1, "The update failed"
    work.day_over(5000, datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    updated = models.Work_day.search_by_parameter(employee.id, datetime.datetime.now().strftime("%Y/%m/%d"))
    assert updated.payment >= 5000, "Work day payment failed"

def test_expenses(category):
    expense = models.Expense(
        id=None,
        name="Test Expense",
        category_id=category.id,
        amount=50000,
        method="Efectivo",
        datetime=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    )
    assert expense.add() != False, "There's a unique contrait fail"
    result = models.Expense.search_by_parameter("name", "Test Expense")
    assert result, "Expense not found after add"
    assert result.amount == 50000, "Expense amount mismatch"
    assert result.categories_id == category.id, "Expense category mismatch"
    result.amount = 75000
    result.update()
    updated = models.Expense.search_by_parameter("name", "Test Expense")
    assert updated.amount == 75000, "Expense update failed"
    result.delete()
    deleted = models.Expense.search_by_parameter("name", "Test Expense")
    assert not deleted, "Expense not deleted"

def test_loans(supplier, config):
    loan = models.Loan(
        id=None,
        supplier_id=supplier.id,
        amount=500000,
        date="2026/06/20",
        installments=3
    )
    assert loan.add() != False, "There's a unique contrait fail"
    result = models.Loan.search_by_parameter("suppliers_id", supplier.id)
    assert result, "Loan not found after add"
    assert result.id != None, "id is not updated"
    assert result.amount == 500000, "Loan amount mismatch"
    assert result.state == "ACTIVE", "Loan state mismatch"
    assert result.installments == 3, "Loan installments mismatch"
    result.determine_payments_dates("MENSUAL")
    installments = config.fetch_by_id('installments_details', result.id, models.Loan.MAIN_TABLE)
    assert installments, "Installments not found"
    for i, installment in enumerate(installments): assert int(installment[3][6]) == 6+i
    assert len(installments) == 3, "Installments count mismatch"
    assert installments[0][5] == "UNPAID", "Installment state mismatch"
    result.update_installment_state(installments[0][0], "PAID", )
    updated = config.fetch_by_id('installments_details', result.id, models.Loan.MAIN_TABLE)
    assert updated, "update failed"
    assert updated[0][5] == "PAID", "Installment state update failed"
    result.delete()
    deleted = models.Loan.search_by_parameter("suppliers_id", supplier.id)
    assert not deleted, "Loan not deleted"

def test_user(config):
    user = models.User(username="test_user", password="test_password")
    user.set_user()
    
    # check password correct
    assert user.check_password(), "Password check failed"
    
    # check wrong password
    wrong_user = models.User(username="test_user", password="wrong_password")
    assert not wrong_user.check_password(), "Wrong password should fail"
    
    # update password
    user.password = "new_password"
    user.update_password()
    
    # delete
    user.delete_user()
    result = models.db.execute_query("SELECT * FROM users WHERE username = ?", ("test_user",))
    assert not result, "User not deleted"

def test_task(config):
    # Add
    task = models.Task(
        id=None,
        name="Pedir mercancía",
        datetime="2026-07-20 09:00:00",
        description="Llamar al proveedor de maquillaje"
    )
    task.add()

    # Search by name
    result = models.Task.search_by_parameter("name", "Pedir mercancía")
    assert result, "task not found after add"
    assert result.state == "PENDING", "task default state mismatch"
    assert result.description == "Llamar al proveedor de maquillaje", "task description mismatch"

    # Search by month
    july_tasks = models.Task.search_by_month("2026", "July")
    assert july_tasks, "No tasks found for July"
    assert any(t.name == "Pedir mercancía" for t in july_tasks), "Task not found in July results"

    # Update state
    result.state = "DONE"
    result.update()
    updated = models.Task.search_by_parameter("name", "Pedir mercancía")
    assert updated.state == "DONE", "Task state update failed"

    # Delete
    result.delete()
    deleted = models.Task.search_by_parameter("name", "Pedir mercancía")
    assert not deleted, "task not deleted"