---
date: 2026-06-17
week: 1
day: 3
until date: 07/04/2026
---
## 🎯 Day goal

- Create classes that will be use like models for the tables
- Add methods to manage it
- Have ready the tests.


## ✅ I did

- [x] Create the models with OOP, defining the attributes and methods.
- [x] Have already all the CRUD in the classes
- [x] create instances, manage the SQL and verify all works
- [x] Over the function to calculate Installments (Ask to my mother for the preferences)


## 🧱 Headaches

- Use tests without edit the database
Solution: Use pytest fixture and create a fiction db that will use the predetermine database in models.

- The pytest had been having problems
Solution: use it with the command python -m to be allocated in the root directory, also create a JSON file called launch to indicate how debug

- The first test put new information in the database that makes failed the other tests
Solution: user the fixture functionality and create a use a temporal database (:memory:)

- Classes seemed in some of their methods.
Solution: use inheritance

- Problems with the unique contrail (SQL respond to the indexes created to avoid something like save the same name).
Solution: For that cases the function will return False (for have differences between errors and no results).

## 💡 learned
- I've learned that the tuple with the * (unpack), can be use to put like single or multiples arguments.
- The SQLite3 execute return a None type, or a list of tuples.
- With vars (python default function), you can represent a class like a dictionary.
- The type hitting, that is python functionality to indicate the type required in situations like a function call, or a instance.
- Understand the list comprehension, that is create a list using a for to make it clean. Follow the next structure:
*(code) for element in elements_another_list -> inside brackets*
- Make multiple tests to check and debug multiples code blocks and use the fixture decorator to complement it and avoid repetition.
- How to transform a datetime object to string (and string to datetime), using strftime and strptime (methods from [[datetime]]), using my own format with the %.
- The datetime objects can be operated between them, it results in a timedelta class. You can access to the hour call the method total_seconds and dividing it by 3600.
- You can put a string to indicate some information from a function, method, class and all the this that could be instance or callable.
- In the venv folder you can access to the libraries util information.
- For the test you need to create a launch file (information in JSON format to make indication to the machine) for debug without problems with the imports.
- You can use the try with a finally clause to make sure that even the program fail, some necessaries lines of code works in all the situations.

## ➡️ Tomorrow

Begin with the UI, (Using web tools), don't forget solve the problems find in test