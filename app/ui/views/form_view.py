import tkinter as tk

class FormView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#282828")

        self.controller = controller

        tk.Label(
            self,
            text="Nome",
            font=("Arial", 18),
            bg="white"
        ).pack(pady=5)

        self.nome_entry = tk.Entry(self)
        self.nome_entry.pack(pady=5)

        tk.Button(self, text="Salvar", command=self.salvar_dados).pack(pady=10)

    def salvar_dados(self):
        nome = self.nome_entry.get()
        print(f"Nome salvo: {nome}")