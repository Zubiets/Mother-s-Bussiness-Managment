from src.database import models, database


inventory = database.Database("data/inventory.db")
print(database.predet_connection(inventory))
models.db = inventory

def main():
    print("Welcome to the Inventory Management System!")
    employee = models.Employee(None, "Test Employee", 6000, "3001234567")
    employee = models.Employee.search_by_parameter("name", "Test Employee")
    if (input("D: ") == "1"):
        work = models.Work_day.search_by_parameter(employee.id, date)
        work.day_over(5000, employee.salary)
    else:
        work = models.Work_day(None, employee.id)

    print(models.Work_day.search_by_parameter(employee.id, ))

if __name__ == "__main__":
    try:
        main()
    finally:
        inventory.disconnect() # Disconnect from the database although will be errors
        print("Goodbye!") 