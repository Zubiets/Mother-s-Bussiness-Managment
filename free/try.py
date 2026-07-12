from tkinter import *

class Try(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label = Label(self, text="Hello, World!")
        self.label.pack()

        self.quit = Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack()

if __name__ == "__main__":
    root = Tk()
    app = Try(master=root)
    app.mainloop()