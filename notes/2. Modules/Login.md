## What does make?

This module will be the main security in the application, its function is not allowed to enter anyone that shouldn't do it. This will be the first window instanced in the application.

## Files

- `src/database/models.py` -> Classes: `User`
- `src/ui/login.py` -> Classes: `Login`, `Verification`


## Technical decisions

- Inside one of the window method if the user put the correct information will instance the app main window.
- I use a image for improve the window screen decoration.
- In all the frames for simplify the some parts, and the simple structure of the login, I use pack method instead of grid for the widgets ([[Custom TKinter]] methods)

## To do

- [x] Add a change password functionality
- [ ] Improve the top window layout
- [ ] When the moment requires, update the window for multiple users

