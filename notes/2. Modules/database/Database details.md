## What does make?
The database will save the information that will be manipulated in the app into SQL tables. This is probably the most important part for a inventory manage app. Will save information within the computer memory in a file called inventory.db

## File

- data/inventory.db
- database/database.py

## Technical decisions
- I've decided to administrate the database with [[SQLite3]] for save information inside the *local memory*, due to isn't necessary bothering with the pay of cloud storage.
- I've decided that the application creates its own database in the code and its tables.
- For the sake of the learning I've decided to create the tables without use the classes
- Not all the classes will represent only one SQL table
- When I was making the classes some behaviors were repeated, hence I decide to use ==*Inheritance*==
- All the function inside database must be based in generic variables

## To do
- [ ] Some day delete the create tables function and replace it with a function in the mother class in models.
- [ ] Figure out how use debugging in pytest module
- [ ] Update the classes to read the excel information
- [ ] Make some day the database based in cloud storage (When I can create the web page)

## relational Links
[[Inventory]]  [[Database structure]]

[^1]: 
