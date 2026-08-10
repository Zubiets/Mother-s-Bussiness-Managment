import tkinter as tk
from tkinter.tix import ROW
import customtkinter as ctk
from ._base import BaseFrame
from src.database.models import Employee, Product, Sale, Category, Supplier, Loan, Expense


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

        for (color, name, clss, headers) in self.INVENTORY_SECTIONS:
            ctk.CTkButton(sections,
                height=40, 
                cursor="hand2",
                hover=False,
                text=name,
                text_color=self.COLORS["text_primary"],
                font=ctk.CTkFont(size=18),
                fg_color=color,
                corner_radius=15,
                command=lambda color=color, clss=clss, headers=headers: self._section_constr(color, clss, headers)
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

        search_frame = ctk.CTkFrame(items_space, fg_color=self.COLORS["card"])
        search_frame.grid(column=0, row=0, sticky="ew", padx=12)
        search_frame.grid_columnconfigure(0, weight=1)
        search_frame.grid_columnconfigure(1, weight=5)
        search_frame.grid_rowconfigure(0, weight=1)

        self.parameter = ctk.StringVar(value="Seleccionar parametro de búsqueda")
        self.parameters_menu = ctk.CTkOptionMenu(search_frame,
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
        )
        self.parameters_menu.grid(row=0, column=0, sticky="ew", padx=12)

        self.search_entry = self.make_entry(search_frame, "Busqueda por nombre de producto")
        self.search_entry.configure(border_color=self.COLORS["bg"])
        self.search_entry.grid(column=1, row=0, sticky="ew", padx=12)
        self.search_entry.bind("<Return>", self._search_product)

        self.view_frame = ctk.CTkFrame(items_space, fg_color=self.COLORS["card"])
        self.view_frame.grid(row=1, column=0, sticky="nsew", padx=12)
        self.view_frame.grid_columnconfigure(0, weight=1)
        self.view_frame.grid_columnconfigure(1, weight=10)
        self.view_frame.grid_rowconfigure(0, weight=1)
        self.view_frame.grid_rowconfigure(1, weight=0)



    def _build_sections(self):
        self.INVENTORY_SECTIONS = {
            ("#F3AC8B", "Productos", Product, ("Nombre", "Precio", "Cantidad", "Estado", "Código QR", "nombre_categoria")),     # light orange
            ("#F8ACDF", "Categorias", Category, ("Nombre", "estado", "Nombre proveedor/es")),                                     # light pink
            ("#C9E8EC", "Ventas", Sale, ("Fecha", "Precio total", "Total pagado", "Metodo de pago", "Descuento en %")),     # light aqua
            ("#A493F3", "Empleados", Employee, ("Nombre", "salario", "Info de contacto", "Estado")),                        # light blue
            ("#F1F79C", "Proveedores", Supplier, ("Nombre/s", "Info de contacto", "Estado")),                                 # light yellow
            ("#E78C8C", "Gastos", Expense, ("Fecha", "Gasto total", "Metodo pago", "Descripcion", "Nombre de la categoria")), # light red
            ("#B8F7AC", "Prestamos", Loan, ("Cantidad", "Fecha", "Cuotas", "Estado", "Nombre del prestador"))         # light green
        }

    def _section_constr(self, color, clss, headers):
        if self.items_tree:
            self.y_scroll.destroy()
            self.x_scroll.destroy()
            self.items_tree.destroy()

        self.configure(fg_color=color)
        self.parameters_menu.configure(values=headers)
        table_data = clss.fetch_table()

        # Scrollbars
        self.y_scroll = ctk.CTkScrollbar(self.view_frame, orientation="vertical")
        self.y_scroll.pack(side="right", fill="y")

        self.x_scroll = ctk.CTkScrollbar(self.view_frame, orientation="horizontal")
        self.x_scroll.pack(side="bottom", fill="x")

        # Treeview
        tk.ttk.Style().configure("Treeview", font=ctk.CTkFont(size=14))
        tk.ttk.Style().configure("Treeview.Heading", font=ctk.CTkFont(size=16))
        self.items_tree = tk.ttk.Treeview(
            self.view_frame,
            columns=headers,
            show="headings",
            yscrollcommand=self.y_scroll.set,
            xscrollcommand=self.x_scroll.set,
        )
        self.items_tree.pack(side="left", fill="both", expand=True)

        # connect scrollbars
        self.y_scroll.configure(command=self.items_tree.yview)
        self.x_scroll.configure(command=self.items_tree.xview)

        for header in headers:
            self.items_tree.heading(header, text=header)

        for row in table_data:
            self.items_tree.insert("", tk.END, values=row)
    
    def _search_product(self, event=None):
        pass