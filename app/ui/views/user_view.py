
from ... import UserController
import tkinter as tk
import tkinter.ttk as ttk
from ..components.generic_table import GenericTable
from pathlib import Path
from datetime import datetime
from bcrypt import hashpw, gensalt


class UserView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#282828")

        self.user_controller = UserController()
        self.controller = controller
        self.edit_mode = False
        self.current_tab = 0
        self.selected_id = None
        self.creatad_at = None

        self._create_headers()
        self._create_notebook()
        self._create_table_tab()
        self._create_form_tab()

        self.set_mode("view")


    def _create_headers(self):
        tk.Label(
            self,
            text="Usuários Cadastrados",
            font=("Arial", 18),
            bg="#282828",
            fg="white"
        ).pack(pady=10)

        current_dir = Path(__file__).resolve().parent
        image_path = current_dir.parent / "images"

        self.save_button_image = tk.PhotoImage(file=image_path / "floppy-disk.png").subsample(3, 3)
        self.delete_button_image = tk.PhotoImage(file=image_path / "delete.png").subsample(3, 3)

        # Frame container
        self.actions_frame = tk.Frame(self, bg="#282828")
        self.actions_frame.pack(fill="x", padx=20, pady=(0,10))

        self.button_new = ttk.Button(
            self.actions_frame,
            text="Novo",
            style="Secondary.TButton",
            command=self.new_user
        )
        self.button_new.pack(side="left", padx=(0, 10))

        self.button_save = ttk.Button(
            self.actions_frame,
            text="Salva",
            image=self.save_button_image,
            compound="left",
            style="Success.TButton",    
            state="disabled",
            command=self.save_user        
        )
        self.button_save.pack(side="left", padx=(0, 10))

        self.button_delete = ttk.Button(
            self.actions_frame,
            text="Exclui",
            image=self.delete_button_image,
            compound="left",
            style="Warning.TButton",
            cursor="hand2",
            state="disabled",
            command= self.delete_user
        )
        self.button_delete.pack(side="left")

        self.button_cancel = ttk.Button(
            self.actions_frame,
            text="Cancelar",
            style="Secondary.TButton",
            state="disabled",
            command=self.cancel_action
        )

        self.button_cancel.pack(side="left", padx=(10, 0))

    

    def _create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)

        # self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        

        self.tab_list = tk.Frame(self.notebook, bg="#282828")
        self.tab_form = tk.Frame(self.notebook, bg="#282828")
        
        self.notebook.add(self.tab_list, text="Listagem")
        self.notebook.add(self.tab_form, text="Formulário")

        self.notebook.tab(1, state="disabled")

    def _create_table_tab(self):
        columns = ["ID", "Nome", "Email", "Matricula", "Criado em", "Atualizado em"]
        raw_data = self.user_controller.list_all()
        
        # Converte os objetos do Peewee (Model instances) para tuplas
        data = []
        if raw_data:
            data = [
                (
                    user.id,
                    user.name,
                    user.email,
                    user.matricula,
                    user.created_at.strftime("%d/%m/%Y %H:%M") if user.created_at else "",
                    user.updated_at.strftime("%d/%m/%Y %H:%M") if user.updated_at else ""
                )
                for user in raw_data
            ]

        self.table = GenericTable(
            self.tab_list,
            columns=columns,
            data=data,            
        )

        self.table.pack(fill="both", expand=True)

       
        # Duplo clique
        self.table.tree.bind("<Double-1>", self.on_double_click)

    def _create_form_tab(self):
       
        form_container = tk.Frame(self.tab_form, bg="#282828")
        form_container.pack(pady=20)

        tk.Label(form_container, text="Email", bg="#282828", fg="white", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_email = ttk.Entry(form_container, width=30, style="Custom.TEntry")
        self.entry_email.grid(row=1, column=1, pady=5)

        tk.Label(form_container, text="Nome", bg="#282828", fg="white", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_name = ttk.Entry(form_container, width=30, style="Custom.TEntry")
        self.entry_name.grid(row=0, column=1, pady=5)

        tk.Label(form_container, text="Matricula", bg="#282828", fg="white", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
        self.entry_matricula = ttk.Entry(form_container, width=30, style="Custom.TEntry")
        self.entry_matricula.grid(row=2, column=1, pady=5)


        tk.Label(form_container, text="Senha", bg="#282828", fg="white", font=("Arial", 12)).grid(row=3, column=0, sticky="w", pady=5)
        self.entry_password = ttk.Entry(form_container, width=30, show="*", style="Custom.TEntry")
        self.entry_password.grid(row=3, column=1, pady=5)

        


    def on_double_click(self, event):
        selected = self.table.tree.selection()
       
        if selected:
            item = self.table.tree.item(selected[0])
            values = item["values"]
            
            self.load_form(values)
            self.edit_mode = True    
            self.set_mode("edit") 

            self.notebook.select(self.tab_form)


    def load_form(self, values):
        self.selected_id = values[0]
        self.entry_name.delete(0, 'end')
        self.entry_name.insert(0, values[1])

        self.entry_email.delete(0, 'end')
        self.entry_email.insert(0, values[2])

        self.entry_matricula.delete(0, 'end')
        self.entry_matricula.insert(0, values[3])
        self.creatad_at = values[4]


       
    def new_user(self):
        self.edit_mode = False
        self.selected_id = None
        self.set_mode("new")
      
        self.notebook.select(self.tab_form)
        

    def save_user(self):
        # id email name matricula password createdAt updattedAt
        name = self.entry_name.get()
        email = self.entry_email.get()
        matricula = self.entry_matricula.get()
        password = self.entry_password.get()
        if password and password.strip():
            # Gera o hash da senha usando bcrypt
            hashed = hashpw(password.encode('utf-8'), gensalt())
            password = hashed.decode('utf-8')

        created_at =  self.creatad_at
        updated_at = datetime.now().strftime("%d/%m/%Y")

        data = {
            "name": name,
            "email": email,
            "matricula": matricula,
            "password": password,
            "created_at": created_at,
            "updated_at": updated_at
        }

        # Passa apenas os campos que têm valores preenchidos
        data = {k: v for k, v in data.items() if v and str(v).strip() != ""}


        if self.mode == "edit" and self.selected_id is not None:
            self.user_controller.update(self.selected_id, data)
            self.set_mode("view")
            self.cancel_action()
            self.refresh_table()
        else:
            # Validação apenas para inserção
            required_fields = ["name", "email", "matricula", "password"]
            missing = [f for f in required_fields if f not in data]
            
            if missing:
                from tkinter import messagebox
                messagebox.showwarning(
                    "Campos Obrigatórios", 
                    f"Os seguintes campos devem ser preenchidos: {', '.join(missing)}"
                )
                return

            retorno = self.user_controller.create(data)
            
            if retorno is True:
                # Caso OK: Volta para a listagem
                self.set_mode("view")
                self.cancel_action()
                self.refresh_table()
            else:
                # Caso ERRO: Mostra erro e fica na tela de formulário
                import json
                from tkinter import messagebox
                error_data = json.loads(retorno)
                
                messagebox.showerror(
                    "Erro ao Criar Usuário", 
                    f"Ocorreu um problema: {error_data.get('message')}\n\nDETALHE: {error_data.get('detail', '')}"
                )

    def delete_user(self):        
        if self.selected_id is not None:           
            print(f"Excluindo usuário {self.selected_id}")
               
            self.user_controller.delete(self.selected_id)
            self.refresh_table()   
            self.set_mode("view")
        else:
            print("Nenhum item selecionado")

    def cancel_action(self):
        self.selected_id = None
        self.entry_name.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_matricula.delete(0, 'end')
        self.entry_password.delete(0, 'end')
        self.set_mode("view")

    def set_mode(self, mode):
        """
        mode:
            'view'
            'edit'
            'new'
        """
        self.mode = mode

        if mode == 'view':
            self.notebook.tab(0, state="normal")
            self.notebook.select(0)

            self.notebook.tab(1, state="disabled")

            self.button_save.config(state="disabled", cursor="arrow")
            self.button_new.config(state="normal", cursor="hand2")
            self.button_delete.config(state="disabled", cursor="arrow")
            self.button_cancel.config(state="disabled", cursor="arrow")

        elif mode in ("edit", "new"):
            self.notebook.tab(0, state="disabled")

            self.notebook.tab(1, state="normal")
            self.notebook.select(1)

            self.button_save.config(state="normal", cursor="hand2")
            self.button_new.config(state="disabled", cursor="arrow")
            self.button_cancel.config(state="normal", cursor="hand2")
            if mode == "edit":
                self.button_delete.config(state="normal", cursor="hand2")
            else:                
                self.button_delete.config(state="disabled", cursor="arrow")

    def refresh_table(self):
        self.table.tree.delete(*self.table.tree.get_children())
                
        raw_data = self.user_controller.list_all()
        if raw_data:
            for user in raw_data:
                self.table.tree.insert(
                    "",
                    "end",
                    iid=str(user.id),
                    values=(
                        user.id,
                        user.name,
                        user.email,
                        user.matricula,
                        user.created_at.strftime("%d/%m/%Y %H:%M") if user.created_at else "",
                        user.updated_at.strftime("%d/%m/%Y %H:%M") if user.updated_at else ""
                    )
                )
