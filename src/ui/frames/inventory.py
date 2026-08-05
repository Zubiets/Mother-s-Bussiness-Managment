from typing import ItemsView

import customtkinter as ctk
from ._base import BaseFrame
from config import INVENTORY_SECTIONS


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

        # space for tab options
        sections = ctk.CTkFrame(body, fg_color="transparent")
        sections.grid(column=0, row=0)

        for (color, name, table) in INVENTORY_SECTIONS:
            ctk.CTkButton(sections,
                height=40, 
                cursor="hand2",
                hover=False,
                text=name,
                text_color=self.COLORS["text_primary"],
                font=ctk.CTkFont(size=18),
                fg_color=color,
                corner_radius=15,
                command=lambda color=color, table=table: self._section_constr(color, table)
            ).pack(side="right", padx=2)

        view = ctk.CTkFrame(body, fg_color="transparent", corner_radius=0)
        view.grid(column=0, row=1, sticky="nsew")
        view.grid_rowconfigure(0, weight=1)
        view.grid_columnconfigure(0, weight=1)

        # space to see the section items
        items_space = self.make_card(view)
        items_space.grid(row=0, column=0, sticky="nsew", padx=12)
        items_space.grid_rowconfigure(0, weight=1)
        items_space.grid_rowconfigure(1, weight=9)
        items_space.grid_columnconfigure(0, weight=1)

        self.search_entry = self.make_entry(items_space, "Busqueda por nombre de producto")
        self.search_entry.grid(column=0, row=0, sticky="ew", padx=12)
        self.search_entry.bind("<Return>", self._search_product)

        items_scrobable = ctk.CTkScrollableFrame(items_space, corner_radius=0, fg_color=self.COLORS["card"],)
        items_scrobable.grid(column=0, row=1, sticky="nsew", padx=12, pady=(0, 12))

    def _section_constr(self, color, table):
        self.configure(fg_color=color)
    
    def _search_product(self, event=None):
        pass