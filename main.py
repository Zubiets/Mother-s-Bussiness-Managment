import src.database

def main():
    print("Welcome to the Inventory Management System!")
    src.database.inventory.disconnect() # Disconnect from the database when the application is closed
    print("Goodbye!")

if __name__ == "__main__":
    main()