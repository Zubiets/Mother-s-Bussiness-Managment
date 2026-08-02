## What does make?
Descripción en 2-3 líneas de qué resuelve.

## Files
- `ui/frame/inventory.py`
- `database/models.py`

## Technical decisions
- I used CTkScrollableFrame due to the product list could be long
- I decide limit the suggestion (5 suggestions MAX), for avoid crashes in the app. Besides only will be showed when the user use the Enter button.
- The price for a more interactive app, will be updated while the users make different actions.
- Floating frames (using place for geometry in the base frame) was used for tecnical respond and suggestions. The respond also will be with color changes.
- Was used the tkinter tool context menu for allowed the user delete different unrequired items


## To do
- [ ] add for the cart section improvements like use the tree from tkinter
- [ ] Swap the icons for images (in config) to have it with colors

## Links
[[Base-de-datos]] [[POS]]