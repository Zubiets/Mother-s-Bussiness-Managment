import customtkinter as ctk
import tkinter as tk
from ._base import BaseFrame
from config import PAYMENT_METHODS
from src.database.models import Sale, Product
import datetime


class PosFrame(BaseFrame):
    def __init__(self, parent, colors):
        super().__init__(parent, colors)
        self.set_header("Caja", "Registra ventas y cobra a los clientes")
        self.cart: list[tuple] = []

    def _build_ui(self):
        body = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        body.grid(row=1, column=0, sticky="nsew", padx=24, pady=16)
        body.grid_columnconfigure(0, weight=5)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        # left column — scan and cart
        left = ctk.CTkFrame(body, fg_color="transparent", corner_radius=0)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(1, weight=1)

        # scan field
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

        self.suggestions_box = self.make_card(self, )

        self.make_label(
            scan_card, "Cantidad",
            size=18, color_key="text_secondary"
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
                                    text_color=self.COLORS["fail"],
                                    font=ctk.CTkFont(size=16),
                                    fg_color=self.COLORS["card"],
                                    corner_radius=10,
                                    border_color=self.COLORS["border"],
                                    border_width=1,
                                    )
        
        # Cart
        cart_card = self.make_card(left)
        cart_card.grid(row=1, column=0, sticky="nsew")
        cart_card.grid_columnconfigure(0, weight=1)
        cart_card.grid_rowconfigure(1, weight=1)

        self.make_label(
            cart_card, "Carrito actual",
            size=18, color_key="text_primary"
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 8))

        self.cart_scroll = ctk.CTkScrollableFrame(
            cart_card,
            fg_color="transparent",
            corner_radius=0,
        )
        self.cart_scroll.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))

        # right column — total and payment
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
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=self.COLORS["accent_text"],
            anchor="w",
        )
        self.total_label.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 14))

        # payment
        payment_card = self.make_card(right)
        payment_card.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        payment_card.grid_columnconfigure(0, weight=5)
        payment_card.grid_columnconfigure(1, weight=4)
        payment_card.grid_columnconfigure(1, weight=1)

        self.make_label(
            payment_card, "Monto recibido",
            size=11, color_key="text_secondary"
        ).grid(row=0, column=0, sticky="w", padx=(16, 8), pady=(14, 6))

        self.payment_entry = self.make_entry(
            payment_card,
            placeholder="$0",
            height=40,
        )
        self.payment_entry.grid(row=1, column=0, sticky="ew", padx=(16, 8), pady=(0, 14))
        self.payment_entry.bind("<KeyRelease>", self._calculate_change)

        # Discount
        self.make_label(
            payment_card, "Descuento al cliente",
            size=11, color_key="text_secondary"
        ).grid(row=0, column=1, sticky="w", padx=8, pady=(14, 6))

        self.discount_entry = self.make_entry(
            payment_card,
            placeholder="0",
            height=40,
        )
        self.discount_entry.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(0, 14))
        self.discount_entry.bind("<KeyRelease>", self._calculate_change)

        ctk.CTkLabel(
            payment_card,
            text="%",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.COLORS["border"],
            anchor="w",
        ).grid(row=1, column=2, sticky="w", padx=5, pady=(0, 14))

        # Change
        change_card = self.make_card(right)
        change_card.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        change_card.grid_columnconfigure(0, weight=1)

        self.make_label(
            change_card, "Cambio",
            size=11, color_key="text_secondary"
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 4))

        self.change_label = ctk.CTkLabel(
            change_card,
            text="$0",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.COLORS["success"],
            anchor="w",
        )
        self.change_label.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 14))

        # pay mathod
        method_card = self.make_card(right)
        method_card.grid(row=3, column=0, sticky="ew", pady=(0, 12))
        method_card.grid_columnconfigure(0, weight=1)

        self.make_label(
            method_card, "Seleccione el metodo de pago",
            size=11, color_key="text_secondary"
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 4))

        self.method = ctk.StringVar(value=PAYMENT_METHODS[0])
        ctk.CTkOptionMenu(method_card,
            height=40,
            values=PAYMENT_METHODS,
            variable=self.method,
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
        ).grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 14))

        # sale button
        self.make_button(
            right, "✓  Confirmar venta",
            command=self._confirm_sale,
            height=48,
        ).grid(row=4, column=0, sticky="ew", pady=(0, 8))

        self.make_button(
            right, "✕  Cancelar",
            command=self._reset_frame,
            accent=False,
            height=36,
        ).grid(row=5, column=0, sticky="ew")

    def _suggest_products(self, event=None):
        for button in self.suggestions_box.winfo_children(): # clean the frame 
            button.destroy()

        product = self.scan_entry.get().strip() # lower is not needed because sql find it anyway
        if not product:
            return

        self.suggestions_box.place(x=40, y=185) # prepare the suggestions frame
        self.suggestions_box.grid_columnconfigure(0, weight=1)
        self.suggestions_box.grid_rowconfigure(4, weight=1)

        suggested_products = Product.suggestion_search("name", product)

        if not suggested_products:
            self.make_label(self.suggestions_box, 
                            text="No se encontro un producto relacionado",
                            color_key="fail",
                            ).grid(row=0, column=0, sticky="ew")
            
        
        for i, p in enumerate(suggested_products):
            self.suggestion_button = ctk.CTkButton(self.suggestions_box,
                                                    width=450,
                                                    fg_color="transparent",
                                                    border_color=self.COLORS["border"],
                                                    border_width=1,
                                                    text_color=self.COLORS["text_secondary"],
                                                    hover_color=self.COLORS["suggest_hover"],
                                                    cursor="hand2",
                                                    font=ctk.CTkFont(size=16),
                                                    text=f"{p.name}{' '*20}{p.price}{' '*20}{p.category}",
                                                    command=lambda product=p: self._on_scan(product),
                                                    )
            self.suggestion_button.grid(row=i, column=0, sticky="ew")

    def _on_scan(self, product: Product):
        amount = self.amount_entry.get().strip()

        if not amount:
            amount = "0"
        
        try:
            amount = int(amount)
        except ValueError:
            self.message_box.place(x=520, y=185)
            self.message.configure(text = "Solo escribir números enteros")
            self.message.pack()
            return

        if amount < 0:
            self.message_box.place(x=520, y=185)
            self.message.configure(text = "Solo escribir números mayores a 0")
            self.message.pack()
            return

        if amount == 0:
            hide_amount = int(tk.simpledialog.askinteger("Confirmar cantidad", "Ingresar cantidad real del producto (No se restara la cantidad total en el local)"))

        if product.amount < amount:
            self.message_box.place(x=420, y=185)
            self.message.configure(text = """La cantidad del producto es menor a la ingresada
            dejar vacio el campo para no registrar cantidad""")
            self.message.pack()
            return


        new_item = (product, amount)

        self.message_box.place_forget()
        self.suggestions_box.place_forget()
        self.cart.append(new_item)

        item_total = product.price*amount
        if item_total == 0:
            item_total = product.price*hide_amount

        current_total = float(self.total_label.cget("text").replace("$", ""))

        self.total_label.configure(text=f"${(current_total+item_total)}")
        
        item_frame = ctk.CTkFrame(self.cart_scroll, 
                                  fg_color="transparent", 
                                  border_color=self.COLORS["border"],
                                  border_width=1,
                                  )
        item_frame.pack(fill="x", pady=5)
        cart_item_text = f"Producto: {product.name}     Cantidad: {amount}     Total: ${item_total}"
        self.item_label = ctk.CTkLabel(item_frame,
                                       text=cart_item_text,
                                       font=ctk.CTkFont(size=16),
                                       text_color=self.COLORS["text_secondary"],
                                       )
        self.item_label.pack(fill='x', pady=2, padx=5)
        self.item_label.bind("<Button-3>", lambda event, item=new_item, frame=item_frame, item_total=item_total: self._context_menu(event, item, frame, item_total))

        self._calculate_change()
        self.amount_entry.delete(0, "end")
        self.scan_entry.delete(0, "end")

    def _context_menu(self, event, item: tuple, frame, item_total: float):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Eliminar", command=lambda item=item, frame=frame, item_total=item_total: self._delete_item(item, frame, item_total))

        try:
            menu.post(event.x_root, event.y_root)
            self.winfo_toplevel().bind("<Button>", lambda e: menu.unpost())
        finally:
            menu.grab_release() # make sure the frame quit even though the app fail

    def _delete_item(self, item: tuple, frame, item_total: float):
        current_total = float(self.total_label.cget("text").replace("$", ""))
        self.total_label.configure(text=f"${current_total-item_total}")
        self._calculate_change()
        self.cart.remove(item)
        frame.destroy()

    def _calculate_change(self, event=None):
        try:
            payment = float(self.payment_entry.get())

            discount_value = self.discount_entry.get()
            if not discount_value:
                discount_value = "0"
            discount = float(discount_value)/100
            if discount > 1 or discount < 0:
                self.discount_entry.configure(border_color=self.COLORS["fail"])
                return

            self.payment_entry.configure(border_color=self.COLORS["border"])
            self.discount_entry.configure(border_color=self.COLORS["border"])

            total = float(self.total_label.cget("text").replace("$", ""))
            change = payment - total*(1-discount)
            self.change_label.configure(
                text=f"${change}",
                text_color=self.COLORS["success"] if change >= 0 else self.COLORS["fail"]
            )
        except ValueError:
            self.payment_entry.configure(border_color=self.COLORS["fail"])
            self.change_label.configure(text="$0", text_color=self.COLORS["success"])

    def _confirm_sale(self):
        try:
            discount = self.discount_entry.get().strip()
            if not discount:
                discount = 0
            sale = Sale(0, 
                datetime=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), 
                total_price=float(self.total_label.cget("text").replace("$", "")),
                payment=float(self.payment_entry.get().strip()),
                method=self.method.get().split(" ", 1)[1],
                discount=int(discount)
            )
            sale.add()
            sale = Sale.search_by_parameter("datetime", sale.datetime)

            for item in self.cart:
                sale.add_sale_detail(*item)

                

            self._reset_frame()
            tk.messagebox.showinfo("Finalizar compra", "La compra ha sido exitosamente registrada", parent=self)



        except ValueError:
            tk.messagebox.showerror("Finalizar compra", "Hay un error con los datos ingresados\n Verificar lugares en rojo", parent=self)

    def _reset_frame(self):
        self.message_box.place_forget()
        self.suggestions_box.place_forget()

        self.amount_entry.delete(0, "end")
        self.scan_entry.delete(0, "end")

        for button in self.suggestions_box.winfo_children(): # clean the frame 
            button.destroy()

        for label in self.cart_scroll.winfo_children(): # clean the frame 
            label.destroy()

        self.cart = []

        self.message_box.place_forget()
        self.suggestions_box.place_forget()

        self.total_label.configure(text="$0")
        self.discount_entry.delete(0, "end")
        self.payment_entry.delete(0,  "end")
        self.change_label.configure(text="$0")

        self.method = ctk.StringVar(value=PAYMENT_METHODS[0])
