import customtkinter as ctk
from ._base import BaseFrame


class PosFrame(BaseFrame):
    def __init__(self, parent, colors):
        super().__init__(parent, colors)
        self.set_header("Caja", "Registra ventas y cobra a los clientes")
        self.products = None

    def _build_ui(self):

        body = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        body.grid(row=1, column=0, sticky="nsew", padx=24, pady=16)
        body.grid_columnconfigure(0, weight=2)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        # Columna izquierda — escaneo y carrito
        left = ctk.CTkFrame(body, fg_color="transparent", corner_radius=0)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(1, weight=1)

        # Campo de escaneo
        scan_card = self.make_card(left)
        scan_card.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        scan_card.grid_columnconfigure(0, weight=9)
        scan_card.grid_columnconfigure(1, weight=1)

        self.make_label(
            scan_card, "Registrar producto",
            size=12, color_key="text_secondary"
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 6))

        self.scan_entry = self.make_entry(
            scan_card,
            placeholder="Escanear QR o ingresar nombre del producto",
            height=40,
        )
        self.scan_entry.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 14))
        self.scan_entry.bind("<Return>", self._suggest_products)
        self.scan_entry.focus()

        self.suggestions_box = ctk.CTkScrollableFrame(self,
                                                      fg_color="transparent",
                                                      border_color=self.COLORS["border"],
                                                      border_width=1,
                                                      )

        self.make_label(
            scan_card, "Cantidad",
            size=12, color_key="text_secondary"
        ).grid(row=0, column=1, sticky="w", padx=16, pady=(14, 6))

        self.amount_entry = self.make_entry(
            scan_card,
            placeholder="0",
            height=40,
        )
        self.amount_entry.grid(row=1, column=1, sticky="w", padx=16, pady=(0, 14))
        self.amount_entry.bind("<Return>", self._suggest_products)

        self.message_box = ctk.CTkFrame(self,
                                        fg_color=self.COLORS["card"],
                                          )

        self.message = ctk.CTkLabel(self.message_box, 
                                    text="Solo escribir números enteros",
                                    text_color=self.COLORS["fail"],
                                    font=ctk.CTkFont(size=15),
                                    fg_color=self.COLORS["card"],
                                    corner_radius=10,
                                    border_color=self.COLORS["border"],
                                    border_width=1,
                                    )
        
        # Carrito
        cart_card = self.make_card(left)
        cart_card.grid(row=1, column=0, sticky="nsew")
        cart_card.grid_columnconfigure(0, weight=1)
        cart_card.grid_rowconfigure(1, weight=1)

        self.make_label(
            cart_card, "Carrito actual",
            size=13, color_key="text_primary"
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 8))

        self.cart_scroll = ctk.CTkScrollableFrame(
            cart_card,
            fg_color="transparent",
            corner_radius=0,
        )
        self.cart_scroll.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self.cart_scroll.grid_columnconfigure(0, weight=1)

        # Columna derecha — total y cobro
        right = ctk.CTkFrame(body, fg_color="transparent", corner_radius=0)
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_columnconfigure(0, weight=1)

        # Total
        total_card = self.make_card(right)
        total_card.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        total_card.grid_columnconfigure(0, weight=1)

        self.make_label(
            total_card, "Total a cobrar",
            size=11, color_key="text_secondary"
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 4))

        self.total_label = ctk.CTkLabel(
            total_card,
            text="$0",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=self.COLORS["accent_text"],
            anchor="w",
        )
        self.total_label.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 14))

        # Monto recibido
        recibido_card = self.make_card(right)
        recibido_card.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        recibido_card.grid_columnconfigure(0, weight=1)

        self.make_label(
            recibido_card, "Monto recibido",
            size=11, color_key="text_secondary"
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 6))

        self.recibido_entry = self.make_entry(
            recibido_card,
            placeholder="$0",
            height=40,
        )
        self.recibido_entry.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 14))
        self.recibido_entry.bind("<KeyRelease>", self._calc_cambio)

        # Cambio
        cambio_card = self.make_card(right)
        cambio_card.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        cambio_card.grid_columnconfigure(0, weight=1)

        self.make_label(
            cambio_card, "Cambio",
            size=11, color_key="text_secondary"
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 4))

        self.cambio_label = ctk.CTkLabel(
            cambio_card,
            text="$0",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.COLORS["success"],
            anchor="w",
        )
        self.cambio_label.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 14))

        # Botón cobrar
        self.make_button(
            right, "✓  Confirmar venta",
            command=self._confirmar_venta,
            height=48,
        ).grid(row=3, column=0, sticky="ew", pady=(0, 8))

        self.make_button(
            right, "✕  Cancelar",
            command=self._cancelar_venta,
            accent=False,
            height=36,
        ).grid(row=4, column=0, sticky="ew")

    def _on_scan(self, event=None):
        code = self.scan_entry.get().strip().lower()
        amount = self.amount_entry.get().strip()

        if not code or not amount:
            return
        
        try:
            amount = int(amount)
        except ValueError:
            self.message_box.place(x=520, y=185)
            self.message.pack()
            return

        self.message_box.place_forget()

        # TODO: buscar producto en models y agregar al carrito

        self.suggestions_box.place_forget()
        self.amount_entry.delete(0, "end")
        self.scan_entry.delete(0, "end")

    def _calc_cambio(self, event=None):
        try:
            recibido = float(self.recibido_entry.get().replace("$", "").replace(".", "").replace(",", "."))
            total = float(self.total_label.cget("text").replace("$", "").replace(".", "").replace(",", "."))
            cambio = recibido - total
            self.cambio_label.configure(
                text=f"${cambio:,.0f}",
                text_color=self.COLORS["success"] if cambio >= 0 else self.COLORS["fail"]
            )
        except ValueError:
            self.cambio_label.configure(text="$0", text_color=self.COLORS["success"])

    def _suggest_products(self, event=None):
        product = self.scan_entry.get().strip().lower()
        if product:
            self.suggestions_box.place(x=40, y=185)
            self.suggestions_box.grid_configure(column=0, row=10)

            for i in range(1, 11):
                self.suggestion_button = ctk.CTkButton(self.suggestions_box,
                                                        width=450,
                                                        fg_color="transparent",
                                                        border_color=self.COLORS["border"],
                                                        border_width=1,
                                                        text_color=self.COLORS["text_secondary"],
                                                        hover_color=self.COLORS["suggest_hover"],
                                                        cursor="hand2",
                                                        text=f"suggestion:{i}",
                                                        )
                self.suggestion_button.grid(row=i, column=0, sticky="ew")

            


    def _confirmar_venta(self):
        # TODO: llamar a models.Sale para guardar la venta
        pass

    def _cancelar_venta(self):
        # TODO: limpiar carrito y resetear totales
        pass