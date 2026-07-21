## 2026-06-15 [[2 SQL DESIGN]] · Problem with the imports
- There are two parts of this problem. In the main module to execute the package you need to import at least one of the functions. The second part is for access to a file or folder in the project, you need to import or put the path like the file were in the root directory, except for the files in the same folder-package.

## 2026-06-15 [[2 SQL DESIGN]] · The first test put new information in the database that makes failed the other tests
- Create with the [[Pytest]] tool; ==Fixture==, a temporal database (RAM based) to avoid edit key information in the main database. The path to this memory space is: :memory:
## 2026-06-25 [[3 Models creation]] · The pytest had been having problems
- use it with the command python -m to be allocated in the root directory, also create a JSON file called launch to indicate how debug
## 2026-07-16 [[4 UI starts]]· VScode didn't recognize Tkinter
- In this occasion the problem was the vs that I had downloaded, it was independent of the system, for that make impossible install some external libraries like Tkinter. The solution was install the Microsoft version online (native btw).
## 2026-07-20 · When a windows is instanced with a bug, it doesn't close.
- No solve yet