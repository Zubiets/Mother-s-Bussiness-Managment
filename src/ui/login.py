import customtkinter as ctk
from tkinter import messagebox
from dotenv import load_dotenv
import os
from screeninfo import get_monitors
from PIL import Image
from config import COLORS
from .app import MainWindow
from src.database.models import User

# upload variables from .env
load_dotenv()

LOGIN_SCREEN_SIZE = 600
VERIFICATION_SCREEN_SIZE = 300
VERTICAL_PIXELS = get_monitors()[0].height
HORIZONTAL_PIXELS = get_monitors()[0].width

ctk.set_appearance_mode = "light"
main_image = ctk.CTkImage(light_image=Image.open("assets/login_wallpaper.jpg"), size=(600, 600))
show_password_image = ctk.CTkImage(light_image=Image.open("assets/show.png"), size=(23, 28))
hide_password_image = ctk.CTkImage(light_image=Image.open("assets/hide.png"), size=(23, 28))

class Login(ctk.CTk):
    x_coor = int(HORIZONTAL_PIXELS/2-LOGIN_SCREEN_SIZE/2)
    y_coor = int(VERTICAL_PIXELS/2-LOGIN_SCREEN_SIZE/2)

    def __init__(self):
        super().__init__()
        self.title("Mandala y Variedades")
        self.geometry(f"{LOGIN_SCREEN_SIZE}x{LOGIN_SCREEN_SIZE}+{self.x_coor}+{self.y_coor}")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["bg"])
        self.verification = None

        self.bind("<Return>", lambda event: self._login())
        self.set_ui()
    
    def set_ui(self):
        wallpaper = ctk.CTkLabel(self, image=main_image)
        wallpaper.place(relx=0.5, rely=0.5, anchor="center")

        frame = ctk.CTkFrame(self, fg_color=COLORS["login"], width=500, height=300)
        frame.place(relx=0.5, rely=0.42, anchor="center")

        label = ctk.CTkLabel(frame, text="Inicio de sesion: Mandala y Variedades", 
                             text_color=COLORS["text_primary"],
                             font=ctk.CTkFont(size=17, weight="bold"),
                             )
        label.pack(pady=5)

        self.entry_user = ctk.CTkEntry(frame,
                                           width=300,
                                           height=50,
                                           placeholder_text="Ingresar usuario",
                                           font=ctk.CTkFont(size=15,),
                                           fg_color=COLORS["login"],
                                           text_color=COLORS["text_secondary"],
                                           corner_radius=15,
                                           border_width=1,
                                           border_color=COLORS["border"]
                                           )
        self.entry_user.pack(pady=5, padx=10)

        self.entry_password = ctk.CTkEntry(frame, show="*",
                                           width=300,
                                           height=50,
                                           placeholder_text="Ingresar contraseña",
                                           font=ctk.CTkFont(size=15,),
                                           text_color=COLORS["text_secondary"],
                                           fg_color=COLORS["login"],
                                           corner_radius=15,
                                           border_width=1,
                                           border_color=COLORS["border"]
                                           )
        self.entry_password.pack(pady=5, padx=10)

        self.show_password_button = ctk.CTkButton(self,
                                width=29,
                                height=30,
                                text="",
                                corner_radius=50,
                                image=show_password_image,
                                fg_color=COLORS["login"],
                                bg_color=COLORS["login"],
                                border_color=COLORS["login"],
                                hover_color=COLORS["card_hover"],
                                cursor="hand2",
                                command=self._showPassword
                            )
        self.show_password_button.place(x=450, y=237)

        login_btn = ctk.CTkButton(frame, 
                                width=300,
                                height=40,
                                text="Iniciar sesión",
                                font=ctk.CTkFont(size=15,),
                                corner_radius=20,
                                fg_color=COLORS["highlight"],
                                hover_color=COLORS["highlight_soft"],
                                cursor="hand2",
                                command=self._login
                            )
        login_btn.pack(pady=7)

        change_pswd_btn = ctk.CTkButton(frame, 
                                width=300,
                                height=40,
                                text="¿contraseña olvidada?",
                                text_color=COLORS["highlight"],
                                font=ctk.CTkFont(size=14,),
                                corner_radius=20,
                                fg_color=COLORS["login"],
                                border_color=COLORS["login"],
                                hover_color=COLORS["card_hover"],
                                cursor="hand2",
                                command=self._verificate,
                            )
        change_pswd_btn.pack(pady=1)

    def _verificate(self):
        if self.verification:
            self.verification.destroy()  # if window exists destroy it  

        self.verification = Verification() 
    
    def _login(self):
            login = User(self.entry_user.get(), self.entry_password.get())
            if login.check_password():
                # messagebox.showinfo("Iniciar sesion", f"Bienvenida {self.entry_user.get()}!", parent=self)
                self.destroy()
                app = MainWindow()
                app.mainloop()
            else:
                messagebox.showerror("Iniciar sesion", "Los datos ingresados son incorrectos", parent=self)
            
    def _showPassword(self):
        if self.entry_password.cget("show") == "*":
            self.entry_password.configure(show="")
            self.show_password_button.configure(image=hide_password_image)
        else:
            self.entry_password.configure(show="*")
            self.show_password_button.configure(image=show_password_image)

class Verification(ctk.CTkToplevel):
    x_coor = int(HORIZONTAL_PIXELS/2-VERIFICATION_SCREEN_SIZE/2)
    y_coor = int(VERTICAL_PIXELS/2-VERIFICATION_SCREEN_SIZE/2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Seguridad")
        self.geometry(f"{VERIFICATION_SCREEN_SIZE}x{VERIFICATION_SCREEN_SIZE}+{self.x_coor}+{self.y_coor}")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["bg"])

        self.bind("<Return>", lambda event: self._changePassword())
        self.build_ui()
    
    def build_ui(self):
        key_label = ctk.CTkLabel(self, 
                                   text="Ingresar la clave de seguridad",
                                   font=ctk.CTkFont(size=17, weight="bold"),
                                   text_color="black",
                                   )
        key_label.pack(pady=(5,0), padx=10)
        self.entry_key = ctk.CTkEntry(self, show="*",
                                width=250,
                                height=35,
                                fg_color="transparent",
                                text_color="black",
                                font=ctk.CTkFont(size=15,)
                                   )
        self.entry_key.pack(pady=(1,4), padx=10)

        user_label = ctk.CTkLabel(self, 
                                   text="Ingresar usuario principal",
                                   font=ctk.CTkFont(size=17, weight="bold"),
                                   text_color="black",
                                   )
        user_label.pack(pady=(5,0), padx=10)

        self.entry_user = ctk.CTkEntry(self, 
                                width=250,
                                height=35,
                                fg_color="transparent",
                                text_color="black",
                                font=ctk.CTkFont(size=15,)
                                )
        self.entry_user.pack(pady=(1,4), padx=10)

        password_label = ctk.CTkLabel(self, 
                                   text="Ingresar la nueva contraseña",
                                   font=ctk.CTkFont(size=17, weight="bold"),
                                   text_color="black")
        password_label.pack(pady=(5,0), padx=10)

        self.entry_password = ctk.CTkEntry(self, show="*",
                                width=250,
                                height=35,
                                fg_color="transparent",
                                text_color="black"
                                      )
        self.entry_password.pack(pady=(1,4), padx=10)

        btn = ctk.CTkButton(self,
                                width=250,
                                height=50,
                                fg_color="black",
                                hover_color="gray",
                                text="Cambiar contraseña",
                                font=ctk.CTkFont(size=16,),
                                cursor="hand2",
                                command=self._changePassword,
                            )
        btn.pack(pady=15)
    
    def _changePassword(self):
        if self.entry_key.get() == os.getenv("RECOVERY_KEY") and self.entry_user.get() == os.getenv("MAIN_USER"):
            updated = User(self.entry_user.get(), self.entry_password.get())
            updated.update_password()
            messagebox.showinfo("Cambiar contraseña", "Contraseña cambiada!", parent=self)
            self.destroy()
        else:
            messagebox.showerror("Cambiar Contraseña", "Los datos ingresados son incorrectos", parent=self)

