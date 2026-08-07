import customtkinter as ctk
from .frames import pos, inventory, employees, expenses, reports, loans, home, tasks
from config import COLORS, NAV_ITEMS, VERSION
from screeninfo import get_monitors

VERTICAL_PIXELS = get_monitors()[0].height
HORIZONTAL_PIXELS = get_monitors()[0].width


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Mandala y Variedades")
        self.geometry(f"{HORIZONTAL_PIXELS}x{VERTICAL_PIXELS}")
        self.minsize(1250, 600)
        self.configure(fg_color=COLORS["bg"])

        self._active = None
        self._nav_buttons = {}


        self._build_layout()
        self._build_sidebar()
        self.build_frames()
        self._navigate("home")

    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            fg_color=COLORS["sidebar"],
            corner_radius=0,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(len(NAV_ITEMS)+2, weight=1)

        self.content = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg"],
            corner_radius=0,
        )
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)


    def _build_sidebar(self):
        title = ctk.CTkButton(
            self.sidebar,
            text="🛍  Mandala y Variedades",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS["sidebar_title"],
            anchor="w",
            fg_color="transparent",
            hover=False,
            cursor="hand2",
            command=lambda k="home": self._navigate(k)
        )
        title.grid(row=0, column=0, padx=16, pady=(20, 16), sticky="ew")

        divider = ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color=COLORS["border"],
        )
        divider.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))

        for i, (icon, label, key) in enumerate(NAV_ITEMS):
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"{icon} {label}", # todo: change the icon to image
                anchor="w",
                height=40,
                corner_radius=18,
                font=ctk.CTkFont(size=15),
                fg_color="transparent",
                text_color=COLORS["text_secondary"],
                hover_color=COLORS["accent_hover"],
                cursor="hand2",
                command=lambda k=key: self._navigate(k),
            )
            btn.grid(row=i + 2, column=0, padx=25, pady=2, sticky="ew")
            self._nav_buttons[key] = btn

        version = ctk.CTkLabel(
            self.sidebar,
            text=VERSION,
            font=ctk.CTkFont(size=12),
            text_color=COLORS["border"],
        )
        version.grid(row=len(NAV_ITEMS)+2, column=0, pady=(0, 25), padx=25, sticky="ws")
    
    def build_frames(self):
            self.frames = {
            "home":      home.HomeFrame(self.content, COLORS),
            "pos":       pos.PosFrame(self.content, COLORS),
            "inventory": inventory.InventoryFrame(self.content, COLORS),
            "employees": employees.EmployeesFrame(self.content, COLORS),
            "expenses":  expenses.ExpensesFrame(self.content, COLORS),
            "reports":   reports.ReportsFrame(self.content, COLORS),
            "loans":     loans.LoansFrame(self.content, COLORS),
            "tasks":     tasks.TasksFrame(self.content, COLORS)
            }

    def _navigate(self, key: str):
        if self._active:
            self._active.grid_remove()

        for k, btn in self._nav_buttons.items():
            if k == key:
                btn.configure(
                    fg_color=COLORS["accent_soft"],
                    text_color=COLORS["text_soft"],
                    hover=False,
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=COLORS["accent_text"],
                    hover=True
                )
        self._active = self.frames[key]
        self._active.grid(row=0, column=0, sticky="nsew")