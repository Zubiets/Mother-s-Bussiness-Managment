from src.ui import windows


def main():
    print("Welcome to the Inventory Management System!")
    app = windows.MainWindow()
    app.mainloop()

if __name__ == "__main__":
    try:
        main()
    finally:
        # inventory.disconnect() # Disconnect from the database although will be errors
        print("Goodbye!") 