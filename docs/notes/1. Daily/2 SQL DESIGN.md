---
date: 2026-06-14
week: 1
day: 2
date 2: 06/15/2026
---

## 🎯 Day goal

Have ready the code for the creation of a SQL table, and make some tests

  

## ✅ I did

- [x] planning the schema of the tables and read the SQLite3 documentation

- [x] make the  code that will create the tables

- [x] create tests and make sure all works

- The [[Database structure]] will use the library SQLite3. See the [[SQLite3 documentation]] for more information

  
## 🧱 Headaches

- Problem with the imports
Solution: There are two parts of this problem. In the main module to execute the package you need to import at least one of the functions. The second part is for access to a file or folder in the project, you need to import or put the path like the file were in the root directory, except for the files in the same folder-package.
- The pytest had been having problems
Solution: use it with the command python -m to be allocated in the root directory.
- The first test put new information in the database that makes failed the other tests
Solution: Delete all information inside the test table.

## 💡 learned

- Create a simple connection using OOP and SQLite3.
- Declarate variables with : for be more descriptive with the type of the variables. Ex: x: int = 25.
- I learned a key concept of python, that is the tuples, that is the way that python save variables of different types in something like the queries, also the results of that queries are not a list, are tuples. Ex: (1, 2, 3) -- 1, a -- 5, -- (). 
- for more information about the last two point see [[Python official documentation]].
- how to make test files using pytest library, [[Pytest documentation]], take on count something like a decorator to erase all the changes made by the test (TO DO).

## ➡️ Tomorrow

Create and have ready the models and the function for data manage