import customtkinter as ctk
from ._base import BaseFrame


class LoansFrame(BaseFrame):
    def __init__(self, parent, colors):
        super().__init__(parent, colors)
        self.set_header("Proveedores", "Gestiona proveedores y préstamos")

    def _build_ui(self):
        placeholder = self.make_label(
            self,
            text="Módulo en construcción...",
            size=14,
            color_key="text_secondary",
        )
        placeholder.grid(row=1, column=0)