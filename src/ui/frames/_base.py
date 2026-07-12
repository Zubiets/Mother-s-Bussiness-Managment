import customtkinter as ctk


class BaseFrame(ctk.CTkFrame):
    """
    Clase base para todos los frames de la app.
    Recibe COLORS del MainWindow para mantener consistencia visual.
    Cada frame hijo debe implementar _build_ui().
    """

    def __init__(self, parent, colors: dict):
        super().__init__(
            parent,
            fg_color=colors["bg"],
            corner_radius=0,
        )
        self.COLORS = colors
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._build_header()
        self._build_ui()

    def _build_header(self):
        self.header = ctk.CTkFrame(
            self,
            fg_color=self.COLORS["bg"],
            corner_radius=0,
            height=60,
        )
        self.header.grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 0))
        self.header.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.header,
            text="",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.COLORS["text_primary"],
            anchor="w",
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        self.subtitle_label = ctk.CTkLabel(
            self.header,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=self.COLORS["text_secondary"],
            anchor="w",
        )
        self.subtitle_label.grid(row=1, column=0, sticky="w")

    def set_header(self, title: str, subtitle: str = ""):
        self.title_label.configure(text=title)
        self.subtitle_label.configure(text=subtitle)

    def make_card(self, parent, **kwargs) -> ctk.CTkFrame:
        return ctk.CTkFrame(
            parent,
            fg_color=self.COLORS["card"],
            corner_radius=12,
            border_width=1,
            border_color=self.COLORS["border"],
            **kwargs,
        )

    def make_label(self, parent, text, size=13, color_key="text_primary", **kwargs):
        return ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(size=size),
            text_color=self.COLORS[color_key],
            **kwargs,
        )

    def make_button(self, parent, text, command, accent=True, **kwargs):
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            fg_color=self.COLORS["accent"] if accent else self.COLORS["card"],
            hover_color=self.COLORS["accent_hover"] if accent else self.COLORS["card_hover"],
            text_color=self.COLORS["text_primary"],
            corner_radius=8,
            font=ctk.CTkFont(size=13),
            **kwargs,
        )

    def make_entry(self, parent, placeholder="", **kwargs):
        return ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            fg_color=self.COLORS["bg"],
            border_color=self.COLORS["border"],
            text_color=self.COLORS["text_primary"],
            placeholder_text_color=self.COLORS["text_secondary"],
            corner_radius=8,
            font=ctk.CTkFont(size=13),
            **kwargs,
        )

    def _build_ui(self):
        """Cada frame hijo implementa aquí su contenido."""
        pass