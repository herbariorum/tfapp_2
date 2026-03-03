import tkinter as tk
from tkinter import ttk

from .views.home_view import HomeView
from .views.form_view import FormView


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TFAPP")
        self.root.geometry("900x500")

        # Configuração do grid principal
        self.root.columnconfigure(0, weight=0) # sidebar fixa       
        self.root.columnconfigure(1, weight=1) # content expande
        self.root.rowconfigure(0, weight=1)

        self._create_style()

        self._create_sidebar()
        self._create_content()

    def _create_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Primary.TButton",
            background="#0d6efd",
            foreground="white",
            padding=6,
            borderwidth=0,
            font=("Helvetica", 12),
            relief="flat",
            focusthickness=3,
            focuscolor="none"
        )

        style.map(
            "Primary.TButton",
            background=[
                ("active", "#0b5ed7"),
                ("pressed", "#0a58ca")
            ]
        )
        
        style.configure(
            "Success.TButton",
            background="#198754",
            foreground="white",
            padding=6,
            relief="flat",
            borderwidth=0,
            focusthickness=3,
            focuscolor="none"
        )

        style.map(
            "Success.TButton",
            background=[
                ("active", "#228B5A"),
                ("pressed", "#157347")
            ],
            foreground=[
                ("active", "white"),
                ("pressed", "white")
            ]
        )

        style.configure(
            "Secondary.TButton",
            background="#6c757d",
            foreground="white",
            padding=6,
            relief="flat",
            borderwidth=0,
            focusthickness=3,
            focuscolor="none"
        )

        style.map(
            "Secondary.TButton",
            background=[
                ("active", "#5c636a"),
                ("pressed", "#565e64")
            ],
            foreground=[
                ("active", "white"),
                ("pressed", "white")
            ]
        )

        style.configure(
            "Warning.TButton",
            background="#ffc107",
            foreground="black",
            padding=6,
            borderwidth=0,
            relief="flat",
            focusthickness=3,
            focuscolor="none"
        )

        style.map(
            "Warning.TButton",
            background=[
                ("active", "#ffc107"),
                ("pressed", "#d39e00")
            ],
            foreground=[
                ("active", "black"),
                ("pressed", "black")
            ]        
        )

        style.configure(
            "Custom.TEntry",
            padding=6,
            relief="flat",
            borderwidth=1,
            fieldbackground="#ffffff",
            background="#ffffff",
            foreground="#212529"
        )

        # ===== ENTRY EM FOCO =====
        style.map(
            "Custom.TEntry",
            bordercolor=[("focus", "#0d6efd")],
            lightcolor=[("focus", "#0d6efd")],
            darkcolor=[("focus", "#0d6efd")]
        )


    def _create_sidebar(self):
        self.sidebar = tk.Frame(self.root, bg="#313131", width=250)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.sidebar.grid_propagate(False) # mantem a largura fixa

        ttk.Button(
            self.sidebar,
            text="Home",
            style="Primary.TButton",
            cursor="hand2",
            command=lambda: self.show_view(HomeView)
        ).pack(fill="x", padx=10, pady=10)

        ttk.Button(
            self.sidebar,
            text="Proprietário",
            style="Primary.TButton",
            cursor="hand2",
            command=lambda: self.show_view(FormView)
        ).pack(fill="x", padx=10, pady=10)
        


    def _create_content(self):
        self.content = tk.Frame(self.root, bg="white")
        self.content.grid(row=0, column=1, sticky="nsew")

        self.current_view = None
        self.show_view(HomeView)

    def show_view(self, view_class):
        if self.current_view is not None:
            self.current_view.destroy()

        self.current_view = view_class(self.content, self)
        self.current_view.pack(fill="both", expand=True)


    def run(self):
        self.root.mainloop()

