from src.database import models, database
import datetime


inventory = database.Database("data/inventory.db")
print(database.predet_connection(inventory))
models.db = inventory

def main():
    print("Welcome to the Inventory Management System!")

if __name__ == "__main__":
    try:
        main()
    finally:
        inventory.disconnect() # Disconnect from the database although will be errors
        print("Goodbye!") 