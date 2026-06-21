from src.database import models, database


def main():
    print("Welcome to the Inventory Management System!")
    print(models.Supplier.search_by_parameter("name", "Felipe Zubieta"))
    inversor = models.Supplier(*tuple(models.Supplier.search_by_parameter("name", "Felipe Zubieta")))
    categoria = models.Category(*tuple(models.Supplier.search_by_parameter("name", "mundial")))
    producto = models.Product
    database.inventory.disconnect() # Disconnect from the database when the application is closed
    print("Goodbye!") 

if __name__ == "__main__":
    main()