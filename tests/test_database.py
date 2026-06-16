# test to ensure the database creation and connection is successful
from src.database.database import Database

def test_create_and_read():
    db = Database('data/inventory.db')
    db.connect()
    db.execute_query("DELETE FROM test")  # clean up before test
    db.create_table('test', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL'
    })
    db.insert_item('test', {'name': 'Test Item'})
    items = db.get_items('test')
    assert len(items) == 1
    db.disconnect()

