# test to ensure the database creation and connection is successful
from src.database import database, models
import datetime
import pytest

@pytest.fixture
def test():
    clean_db = database.Database("")
    database.predet_connection(clean_db)
    assert clean_db.connection is not None, "Database connection should be established"

    models.db = clean_db
    yield clean_db

    clean_db.disconnect()

def test_database(test):
    # verificar creacion exitosa
    buffer = models.Supplier(0, "Prueba", "Celular: 123456789")
    buffer.add()
    supplier = models.Supplier.search_by_parameter("name", buffer.name)
    assert supplier is not None
    inversor = models.Supplier(*tuple(supplier))
    assert inversor.id == 1
    assert inversor.name == buffer.name
    assert inversor.contact_info == buffer.contact_info
