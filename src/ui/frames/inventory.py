import customtkinter as ctk
from ._base import BaseFrame


class InventoryFrame(BaseFrame):
    def __init__(self, parent, colors):
        super().__init__(parent, colors)
        self.set_header("Inventario", "Administra productos y categorías")

    def _build_ui(self):
        body = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        body.grid(row=1, column=0, sticky="nsew", padx=24, pady=16)
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(0, weight=1)
        body.grid_rowconfigure(1, weight=9)

        sections = ctk.CTkTabview(body, 
            
        )
