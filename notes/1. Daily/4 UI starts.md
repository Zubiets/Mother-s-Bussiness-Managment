---
date: 2026-07-05
week: 1
day: 3
date until: 06/15/2026
---

## 🎯 Day goal

  - Have ready the login and the first frame



## ✅ I did


- [x] Learn about CTK in [[Custom TKinter]].

- [x] Have the app base with a good structure, color and design

- [x] Over the login window

- [x] Make the first frame: POS

- I put some new modifications to models during the process of the UI construction.
- The [[Database structure]] will use the library SQLite3. See the [[SQLite3]] for more information

  

## 🧱 Headaches

- VScode didn't recognize Tkinter
solution: In this occasion the problem was the vs that I had downloaded, it was independent of the system, for that make impossible install some external libraries like Tkinter. The solution was install the Microsoft version online (native btw).  

- The last accent of the sidebar is put apart of the rest.
Solution: When was created the limit of rows, is important that it depends on the number of items in navigate items list

- The last frame created is the only one is showed on the screen.
Solution: The build method created all at the same time, the problem is when the user didn't select the last frame, it wasn't going to change to another frame. For solve this i decide to replace the original build, to another that only create a new home frame (for defect will be activated, and it'll can't be eliminated). The other frames only when will be press their button will be created.

- The windows is put in the screen corner
Solution: using [[screen info]] we can get the PC dimensions, and with these, calculate the position where the windows will be in the center

- When was tried to search for a product to sale the app make the process slow.
solution: limit the inquiry results.

- Some of the right side cards didn't show in the screen.
solution: One could've been to change the POS frame to a scrobbable frame, but for the sake of my mother sight, I decide to mix some entries.

- Decide how to respond the users errors was too tricky.
Solution: For the search errors I decided to add a frame with place for make it like a floating frame, the payment errors only the entry border that the erros was made will chage its color to red.
  
## 💡 learned

  

- Create a simple connection using OOP and SQLite3.

- Declarate variables with : for be more descriptive with the type of the variables. Ex: x: int = 25.

- I learned a key concept of python, that is the tuples, that is the way that python save variables of different types in something like the queries, also the results of that queries are not a list, are tuples. Ex: (1, 2, 3) -- 1, a -- 5, -- ().

- for more information about the last two point see [[*Python official documentation*]].

- how to make test files using pytest library, [[Pytest]], take on count something like a decorator to erase all the changes made by the test (TO DO).

- create interactive and consistent design with CTk where although I had a lot of problems, I consider is one of the easiest UI frameworks.

- The context menu, a tool present in all the apps that we've ever used.

## ➡️ Tomorrow

make the inventory frame and the home base frame (even if all going good, make it all without charts until the moment)