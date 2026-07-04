import pytest
from src.database import database, models
import datetime

@pytest.fixture
def config():
    clean_db = database.Database(":memory:")
    print(database.predet_connection(clean_db))
    assert clean_db.connection is not None, "Database connection should be established"
    models.db = clean_db
    yield clean_db
    clean_db.disconnect()

@pytest.fixture
def supplier(config):
    s = models.Supplier(id=None, name="Test Supplier", contact_info="123456789")
    s.add()
    return models.Supplier.search_by_parameter("name", "Test Supplier")

@pytest.fixture
def category(supplier):
    c = models.Category(id=None, name="Test Category", supplier_id=supplier.id, description="Test description")
    c.add()
    return models.Category.search_by_parameter("name", "Test Category")

@pytest.fixture
def product(category):
    p = models.Product(id=None, name="Test Product", category_id=category.id, price=5000, qr_code="TEST123")
    p.add()
    return models.Product.search_by_parameter("name", "Test Product")

@pytest.fixture
def sale(product):
    s = models.Sale(id=None, datetime=datetime.datetime.now(), total_price=0, discount=0)
    s.add()
    return models.Sale.search_by_parameter("total_price", 0)

@pytest.fixture
def employee(config):
    e = models.Employee(id=None, name="Test Employee", salary=1500000, contact="3001234567")
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

def test_sales(sale, product):
    assert sale, "Sale not found after add"
    assert sale.total_price == 0, "Sale total price mismatch"
    sale.add_sale_detail(product_id=product.id, quantity=2, price=5000)
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
        id=None,
        employee_id=employee.id,
        date="2026-06-20",
        time_in=str(datetime.datetime.now())
    )
    result = models.Work_day.search_by_parameter(employee.id, "2026-06-20")
    assert result, "Work day not found after add"
    work = models.Work_day(*result[0]) if isinstance(result, list) else result
    assert work.employee_id == employee.id, "Work day employee mismatch"
    work.day_over(
        extra=0,
        salary=employee.salary,
        time_out=str(datetime.datetime.now())
    )
    work.update()
    updated = models.Work_day.search_by_parameter(employee.id, "2026-06-20")
    assert updated.payment > 0, "Work day payment not calculated"

def test_expenses(category):
    expense = models.Expense(
        id=None,
        name="Test Expense",
        category_id=category.id,
        amount=50000,
        datetime=datetime.datetime.now()
    )
    expense.add()
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
        loan_date="2026-06-20",
        installments=3
    )
    loan.add()
    result = models.Loan.search_by_parameter("suppliers_id", supplier.id)
    assert result, "Loan not found after add"
    assert result.id != None, "id is not updated"
    assert result.amount == 500000, "Loan amount mismatch"
    assert result.state == "ACTIVE", "Loan state mismatch"
    assert result.installments == 3, "Loan installments mismatch"
    result.determine_payments_dates("MONTHLY")
    installments = config.fetch_by_id(models.Loan.MAIN_TABLE, result.id, models.Loan.SECONDARY_TABLE)
    assert installments, "Installments not found"
    assert len(installments) == 3, "Installments count mismatch"
    assert installments[0][4] == "UNPAID", "Installment state mismatch"
    result.update_installment_state(installments[0][0], "PAID")
    updated = config.fetch_by_id(models.Loan.MAIN_TABLE, loan.id, models.Loan.SECONDARY_TABLE)
    assert updated[0][4] == "PAID", "Installment state update failed"
    result.delete()
    deleted = models.Loan.search_by_parameter("suppliers_id", supplier.id)
    assert not deleted, "Loan not deleted"