import customtkinter as ctk
from ._base import BaseFrame


class HomeFrame(BaseFrame):
    def __init__(self, parent, colors):
        super().__init__(parent, colors)
    
    def _build_header(self):
        pass

    def _build_ui(self):
        self.grid_rowconfigure(0, weight=1)
        
        body = ctk.CTkFrame(self, width=200, height=900, fg_color="red")
        body.grid(row=0, column=0, sticky="n" )