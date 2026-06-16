from .database import inventory, create_tables

create_tables()
inventory.disconnect()