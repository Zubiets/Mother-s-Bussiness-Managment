import pytest
from src.database import database, models
import datetime

@pytest.fixture
def test_db():
    clean_db = database.Database(":memory:")
    database.predet_connection(clean_db)
    assert clean_db.connection is not None, "Database connection should be established"
    models.db = clean_db
    yield clean_db
    clean_db.disconnect()

@pytest.fixture
def supplier(test_db):
    s = models.Supplier(id=None, name="Test Supplier", contact_info="123456789")
    s.add()
    return models.Supplier.search_by_parameter("name", "Test Supplier")

@pytest.fixture
def category(supplier):
    c = models.Category(id=None, supplier_id=supplier.id, name="Test Category")
    c.add()
    return models.Category.search_by_parameter("name", "Test Category")

@pytest.fixture
def product(category):
    p = models.Product(id=None, name="Test Product", category_id=category.id, amount=3, price=5000, qr_code="TEST123")
    p.add()
    return models.Product.search_by_parameter("name", "Test Product")

@pytest.fixture
def sale(test_db):
    s = models.Sale(
        id=None,
        datetime=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        total_price=0,
        discount=0
    )
    s.add()
    return models.Sale.search_by_parameter("total_price", 0)

@pytest.fixture
def employee(test_db):
    e = models.Employee(id=None, name="Test Employee", salary=1500000, contact="3001234567")
    e.add()
    return models.Employee.search_by_parameter("name", "Test Employee")

def test_suppliers(supplier):
    assert supplier, "Supplier not found after add"
    assert supplier.name == "Test Supplier", "Supplier name mismatch"
    assert supplier.contact_info == "123456789", "Supplier contact mismatch"
    assert supplier.state == "ACTIVE", "Supplier state mismatch"
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
    assert category.state == "ACTIVE", "Category state mismatch"
    category.delete()
    result = models.Category.search_by_parameter("name", "Test Category")
    assert not result, "Category not deleted"

def test_products(product, category):
    assert product, "Product not found after add"
    assert product.price == 5000, "Product price mismatch"
    assert product.state == "ACTIVE", "Product state mismatch"
    assert product.categories_id == category.id, "Product category mismatch"
    assert product.qr_code == "TEST123", "Product qr_code mismatch"
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

def test_sales(sale, product):
    assert sale, "Sale not found after add"
    assert sale.total_price == 0, "Sale initial total mismatch"
    sale.add_sale_detail(product=product, amount=2)
    assert sale.total_price == 10000, "Sale total after detail mismatch"
    details = sale.get_sale_details()
    assert details, "Sale details not found"
    assert len(details) == 1, "Unexpected number of sale details"
    assert details[0][1] == 2, "Sale detail quantity mismatch"
    assert details[0][2] == 5000, "Sale detail price mismatch"
    updated_product = models.Product.search_by_parameter("name", "Test Product")
    assert updated_product.amount == 1, "Product stock not reduced after sale"
    sale.total_price = 80000
    sale.update()
    updated = models.Sale.search_by_parameter("total_price", 80000)
    assert updated.total_price == 80000, "Sale update failed"
    sale.delete()
    result = models.Sale.search_by_parameter("total_price", 80000)
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
    today = datetime.datetime.now().strftime("%Y/%m/%d")
    time_in = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    work = models.Work_day(
        id=None,
        employee_id=employee.id,
        date=today,
        time_in=time_in
    )
    work.add()
    records = models.Work_day.search_by_parameter(employee.id, today)
    assert records, "Work day not found after add"
    work = records[0]
    assert work.employee_id == employee.id, "Work day employee mismatch"
    time_out = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    work.day_over(extra=5000, time_out=time_out)
    updated = models.Work_day.search_by_parameter(employee.id, today)
    assert updated, "Work day not found after update"
    assert updated[0].payment >= 0, "Work day payment not calculated"
    assert updated[0].state == "UNPAID", "Work day state mismatch"

def test_expenses(category):
    expense = models.Expense(
        id=None,
        category_id=category.id,
        description="Test Expense",
        amount=50000,
        method="Efectivo",
        datetime=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    )
    expense.add()
    result = models.Expense.search_by_parameter("datetime", expense.datetime)
    assert result, "Expense not found after add"
    assert result.amount == 50000, "Expense amount mismatch"
    assert result.categories_id == category.id, "Expense category mismatch"
    assert result.payment_method == "Efectivo", "Expense method mismatch"
    result.amount = 75000
    result.update()
    updated = models.Expense.search_by_parameter("datetime", expense.datetime)
    assert updated.amount == 75000, "Expense update failed"
    result.delete()
    deleted = models.Expense.search_by_parameter("datetime", expense.datetime)
    assert not deleted, "Expense not deleted"

def test_loans(supplier):
    loan = models.Loan(
        id=None,
        supplier_id=supplier.id,
        amount=500000,
        date="2026/06/20",
        installments=3
    )
    loan.add()
    result = models.Loan.search_by_parameter("suppliers_id", supplier.id)
    assert result, "Loan not found after add"
    assert result.amount == 500000, "Loan amount mismatch"
    assert result.state == "ACTIVE", "Loan state mismatch"
    assert result.installments == 3, "Loan installments mismatch"
    result.determine_payments_dates("MENSUAL")
    installments = result.fetch_installments()
    assert installments, "Installments not found"
    assert len(installments) == 3, "Installments count mismatch"
    assert installments[0][5] == "UNPAID", "Installment initial state mismatch"
    result.update_installment_state(installments[0][0], "PAID", "Efectivo")
    updated = result.fetch_installments()
    assert updated[0][5] == "PAID", "Installment state update failed"
    result.delete()
    deleted = models.Loan.search_by_parameter("suppliers_id", supplier.id)
    assert not deleted, "Loan not deleted"

def test_user(test_db):
    user = models.User(username="test_user", password="test_password")
    user.set_user()
    assert user.check_password(), "Password check failed"
    wrong_user = models.User(username="test_user", password="wrong_password")
    assert not wrong_user.check_password(), "Wrong password should fail"
    user.password = "new_password"
    user.update_password()
    updated_user = models.User(username="test_user", password="new_password")
    assert updated_user.check_password(), "Updated password check failed"
    user.delete_user()
    result = models.db.execute_query("SELECT * FROM users WHERE username = ?", ("test_user",))
    assert not result, "User not deleted"

def test_task(test_db):
    task = models.Task(
        id=None,
        name="Pedir mercancía",
        datetime="2026/07/20 09:00:00",
        description="Llamar al proveedor de maquillaje"
    )
    task.add()
    result = models.Task.search_by_parameter("name", "Pedir mercancía")
    assert result, "Task not found after add"
    assert result.state == "PENDING", "Task default state mismatch"
    assert result.highlight == "DEACTIVATE", "Task highlight mismatch"
    assert result.description == "Llamar al proveedor de maquillaje", "Task description mismatch"
    july_tasks = models.Task.search_by_month("2026", "July")
    assert july_tasks, "No tasks found for July"
    assert any(t.name == "Pedir mercancía" for t in july_tasks), "Task not found in July"
    result.state = "DONE"
    result.update()
    updated = models.Task.search_by_parameter("name", "Pedir mercancía")
    assert updated.state == "DONE", "Task state update failed"
    result.highlight = "ACTIVATE"
    result.update()
    highlighted = models.Task.search_by_parameter("name", "Pedir mercancía")
    assert highlighted.highlight == "ACTIVATE", "Task highlight update failed"
    result.delete()
    deleted = models.Task.search_by_parameter("name", "Pedir mercancía")
    assert not deleted, "Task not deleted"

def test_suggestion_search(category):
    for i in range(3):
        p = models.Product(
            id=None,
            name=f"Test Product {i}",
            category_id=category.id,
            price=1000 * (i + 1),
            qr_code=f"QR00{i}"
        )
        p.add()
    results = models.Product.suggestion_search("name", "Test Product")
    assert results, "No suggestions found"
    assert isinstance(results, list), "Should return a list"
    assert len(results) == 3, "Should find 3 products"
    assert all(hasattr(r, 'name') for r in results), "Each result should be a Product instance"
    partial = models.Product.suggestion_search("name", "Product 1")
    assert partial, "Partial match not found"
    assert len(partial) == 1, "Should find only 1 partial match"
    results[0].state = "INACTIVE"
    results[0].update()
    active_results = models.Product.suggestion_search("name", "Test Product")
    assert len(active_results) == 2, "Inactive products should be excluded"
    all_results = models.Product.search_by_parameter("state", "ACTIVE")
    assert isinstance(all_results, list), "Multiple results should return list"

def test_fetchall(test_db):
    s = models.Supplier(id=None, name="Fetch Test", contact_info="3001111111")
    s.add()
    result = test_db.fetch_table("suppliers")
    assert result, "fetch_table returned no results"
    assert len(result) >= 1, "Should have at least one row"

    e2 = models.Supplier(id=None, name="Fetch test 2", contact_info="312221222")
    e2.add()
    result2 = models.Supplier.fetch_table()
    assert result2, "fetch method has not result"
    assert len(result2) == 2, "the table must have 2 rows"

    c = models.Category(id=None, supplier_id=result2[1][0], name="Fetch test 3")
    c.add()
    result3 = models.Category.fetch_table()
    assert result3, "categories fetch has no result"
    assert len(result3) == 1, "The table must have one row"

