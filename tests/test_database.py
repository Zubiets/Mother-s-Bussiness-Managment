# test to ensure the database creation and connection is successful
from src.database import inventory

def test_database():
    assert inventory.connection is not None, "Database connection should be established"
    inventory.create_table('test', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'description': 'TEXT NOT NULL'
    })
    inventory.execute_query("DELETE FROM test")  # clean up before test

    inventory.insert_item('test', {'name': 'Test Item', 'description': 'This is a test item'})
    inventory.insert_item('test', {'name': 'Another Item', 'description': 'This is another test item'})
    items = inventory.execute_query("SELECT * FROM test")
    assert len(items) == 2 , "There should be 2 rows in the test table"

    item1_id = items[0][0]
    item2_id = items[1][0]

    inventory.update_item('test', item1_id, {'name': 'Updated Item 1', 'description': 'This is an updated test item 1'})
    inventory.update_item('test', item2_id, {'name': 'Updated Item 2', 'description': 'This is an updated test item 2'})
    updated_item1 = inventory.execute_query("SELECT * FROM test WHERE id = ?", (item1_id,))
    updated_item2 = inventory.execute_query("SELECT * FROM test WHERE id = ?", (item2_id,))
    assert updated_item1[0][1] == 'Updated Item 1'
    assert updated_item2[0][1] == 'Updated Item 2'

    inventory.disconnect()

