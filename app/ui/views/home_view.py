
import tkinter as tk
import tkinter.ttk as ttk

from .user_view import UserView


class HomeView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#282828")

        self.controller = controller


        tk.Label(
            self,
            text="TFAGRO APP",
            font=("Arial", 18),
            bg="#282828",
            fg="white"
        ).pack(pady=20)

        tk.Label(
            self,
            text="Bem-vindo à aplicação",
            bg="#282828",
            fg="white"         
        ).pack(
            pady=10
        )

        ttk.Button(
            self,
            text="Cadastrar usuário",
            style="Warning.TButton",
            cursor="hand2",
            command=lambda: self.cadastrar_usuario(),
            ).pack(pady=10)
        

    def cadastrar_usuario(self):
        self.controller.show_view(UserView)