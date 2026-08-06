import tkinter as tk
import customtkinter as ctk
from ._base import BaseFrame
from src.database.models import fetch_table

class InventoryFrame(BaseFrame):
    def __init__(self, parent, colors):
        self._build_sections()
        super().__init__(parent, colors)
        self.set_header("Inventario", "Administra productos y categorías")
        self.items_tree = None
        

    def _build_ui(self):
        body = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        body.grid(row=1, column=0, sticky="nsew", padx=24, pady=16)
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(0, weight=1)
        body.grid_rowconfigure(1, weight=9)

        # space for tab options
        sections = ctk.CTkFrame(body, fg_color="transparent")
        sections.grid(column=0, row=0)

        for (color, name, table, headers) in self.INVENTORY_SECTIONS:
            ctk.CTkButton(sections,
                height=40, 
                cursor="hand2",
                hover=False,
                text=name,
                text_color=self.COLORS["text_primary"],
                font=ctk.CTkFont(size=18),
                fg_color=color,
                corner_radius=15,
                command=lambda color=color, table=table, headers=headers: self._section_constr(color, table, headers)
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

        search_space = ctk.CTkFrame(items_space, fg_color=self.COLORS["card"])
        search_space.grid(column=0, row=0, sticky="ew", padx=12)
        search_space.grid_columnconfigure(0, weight=1)
        search_space.grid_columnconfigure(1, weight=5)
        search_space.grid_rowconfigure(0, weight=1)

        self.parameter = ctk.StringVar()
        ctk.CTkOptionMenu(search_space,
            variable=self.parameter,
            values=[],
            fg_color=self.COLORS["bg"],
            button_color=self.COLORS["bg"],
            button_hover_color=self.COLORS["bg"],
            text_color=self.COLORS["text_secondary"],
            corner_radius=8,    
            dropdown_fg_color=self.COLORS["bg"],
            dropdown_hover_color=self.COLORS["card_hover"],
            dropdown_text_color=self.COLORS["text_secondary"],
            font=ctk.CTkFont(size=16),
            dropdown_font=ctk.CTkFont(size=15),
            cursor="hand2",
        ).grid(row=0, column=0, sticky="ew", padx=12)

        self.search_entry = self.make_entry(search_space, "Busqueda por nombre de producto")
        self.search_entry.configure(border_color=self.COLORS["bg"])
        self.search_entry.grid(column=1, row=0, sticky="ew", padx=12)
        self.search_entry.bind("<Return>", self._search_product)

        self.items_scrobable = ctk.CTkScrollableFrame(items_space, corner_radius=0, fg_color=self.COLORS["card"],)
        self.items_scrobable.grid(column=0, row=1, sticky="nsew", padx=12, pady=(0, 12))

    def _build_sections(self):
        self.INVENTORY_SECTIONS = {
            ("#F3AC8B", "Productos", "products", ("ID", "Nombre", "ID categoria", "Precio", "Cantidad", "Estado", "Código QR")),     # light orange
            ("#F8ACDF", "Categorias", "categories", ("id", "Nombre", "id proveedor", "estado")),                                     # light pink
            ("#C9E8EC", "Ventas", "sales", ("ID", "Fecha", "Precio total", "Total pagado", "Metodo de pago", "Descuento en %")),     # light aqua
            ("#A493F3", "Empleados", "employees", ("ID", "Nombre", "salario", "Info de contacto", "Estado")),                        # light blue
            ("#F1F79C", "Proveedores", "suppliers", ("ID", "Nombre", "Info de contacto", "Estado")),                                 # light yellow
            ("#E78C8C", "Gastos", "Expenses", ("ID", "Nombre", "ID categoria", "Gasto total", "Metodo pago", "Fecha", "código QR")), # light red
            ("#B8F7AC", "Prestamos", "Loans", ("ID", "ID proveedor", "Cantidad", "Fecha", "Cuotas", "Estado"))         # light green
        }

    def _section_constr(self, color, table, headers):
        if self.items_tree:
            self.items_tree.destroy()

        self.configure(fg_color=color)
        table_result = fetch_table(table)
        self.items_tree = tk.ttk.Treeview(self.items_scrobable, columns=list(table_result[0].keys()), show="headings")
        self.items_tree.pack()

        for i, header in enumerate(headers):
            self.items_tree.heading(list(table_result[0].keys())[i], text=header)


    
    def _search_product(self, event=None):
        pass