## Description
SQLite3 is the library that will be useful for connect and execute SQL code into our principal database.
## Tools
- connect() and close(): These are library methods that will have the job of take the database name (file path) and close it when is necessary.
- cursor() and execute(): These a connection method and a cursor method that will permit execute different SQL command, first you instance a cursor with the cursor method, then you use execute with two arguments, a string with the command and a tuple to cover the spaces with ? signals. Take on that.
- Commit(), fetchone() and fetchall(): These are methods to save the changes in the database, and return one and more elements if the query requires
## Link:
- Page:
[https://docs.python-guide.org/writing/structure/](https://docs.python.org/3/library/sqlite3.html#tutorial)