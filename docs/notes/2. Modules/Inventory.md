## What does make?
This module will have the work of manage the business database, where will have all the functions and classes, and the GUI that will use them.

## Files
- `src/ui/inventory_view.py`
- `src/database/models.py`

## Technical decisions
- All the queries will only exist in this module files for the sake of the project consistent
- The database connection will be made in the main file to use the db references in models and the table creation like predetermine for future uses.
- To avoid unexpected errors while the app is working, I've decided to add a strong correlation with [[Test]]

## To do
- [x] make a responsive for the error in the database that cannot be catch in the code
- [ ] over the test with using AI