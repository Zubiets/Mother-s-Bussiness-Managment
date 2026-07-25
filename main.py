import os
from dotenv import load_dotenv
from src.ui import app
from src.database import database, models

# upload variables from .env
load_dotenv()


def main():
    print("Welcome to the Inventory Management System!")

    db = database.Database("data/inventory.db")
    database.predet_connection(db)
    models.db = db

    if not db.fetch_table("users"):
        default = models.User(os.getenv("MAIN_USER"), os.getenv("PASSWORD"))
        default.set_user()

    login = app.MainWindow()
    login.mainloop()

if __name__ == "__main__":
    try:
        main()
    finally:
        # inventory.disconnect() # Disconnect from the database although will be errors
        print("Goodbye!") 