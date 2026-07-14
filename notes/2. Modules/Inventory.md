## What does make?
This module will have the work of manage the business database, where will have all the functions and classes, and the GUI that will use them.

## Files
- `src/ui/frames/inventory.py`
- `src/database/models.py`

## Technical decisions
- All the queries will only exist in this module files for the sake of the project consistent
- The database connection will be made in the main file to use the db references in models and the table creation like predetermine for future uses.
- To avoid unexpected errors while the app is working, I've decided to add a strong correlation with [[Test]]
- All the dates must be convert to string to avoid version problems (SQLite3 warning).
- To avoid problems with unexpected calls, the UI and the main will have the responsibility of call most of the attributes and methods in models, and some methods of database
- For cases where can exist a query error, the function will return false to make a respond in the UI.

## To do
- [x] make a responsive for the error in the database that cannot be catch in the code
- [x] over the test with using AI