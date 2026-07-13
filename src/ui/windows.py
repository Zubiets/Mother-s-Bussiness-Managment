import customtkinter as ctk
from .frames import pos, inventory, suppliers, employees, expenses, reports, loans
from config import COLORS, NAV_ITEMS

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Variedades — Gestión")
        self.minsize(900, 600)
        self.geometry("1200x750")
        self.configure(fg_color=COLORS["bg"])

        self._active = None
        self._nav_buttons = {}

        self._build_layout()
        self._build_sidebar()
        self._builds()
        self._navigate("caja")

    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(
            self,
            width=200,
            fg_color=COLORS["sidebar"],
            corner_radius=0,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(8, weight=1)

        self.content = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg"],
            corner_radius=0,
        )
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

    def _build_sidebar(self):
        logo = ctk.CTkLabel(
            self.sidebar,
            text="🛍  Mandala y Variedades",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        )
        logo.grid(row=0, column=0, padx=16, pady=(20, 16), sticky="ew")

        divider = ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color=COLORS["border"],
            corner_radius=0,
        )
        divider.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))

        for i, (icon, label, key) in enumerate(NAV_ITEMS):
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"  {label}",
                anchor="w",
                height=40,
                corner_radius=10,
                font=ctk.CTkFont(size=13),
                fg_color="transparent",
                text_color=COLORS["text_secondary"],
                hover_color=COLORS["card"],
                command=lambda k=key: self._navigate(k),
            )
            btn.grid(row=i + 2, column=0, padx=10, pady=2, sticky="ew")
            self._nav_buttons[key] = btn

        version = ctk.CTkLabel(
            self.sidebar,
            text="v1.0.0",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["border"],
        )
        version.grid(row=9, column=0, pady=(0, 16))

    def _builds(self):
        self.s = {
            "caja":      pos.PosFrame(self.content, COLORS),
            "inventario": inventory.InventoryFrame(self.content, COLORS),
            "suppliers": suppliers.SuppliersFrame(self.content, COLORS),
            "employees": employees.EmployeesFrame(self.content, COLORS),
            "expenses":  expenses.ExpensesFrame(self.content, COLORS),
            "reports":   reports.ReportsFrame(self.content, COLORS),
            "loans": loans.LoansFrame(self.content, COLORS)
        }
        for frame in self.s.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def _navigate(self, key: str):
        if self._active:
            self._active.grid_remove()

        for k, btn in self._nav_buttons.items():
            if k == key:
                btn.configure(
                    fg_color=COLORS["accent_soft"],
                    text_color=COLORS["accent"],
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=COLORS["text_secondary"],
                )

        self._active = self.s[key]
        self._active.grid()