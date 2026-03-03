import tkinter as tk
import tkinter.ttk as ttk

class GenericTable(tk.Frame):
    def __init__(self, parent, columns, data, column_widths=None):
        super().__init__(parent)

        self.columns = columns
        self.data = data

        self._create_style()

        self.tree = ttk.Treeview(
            self,
            columns=self.columns,
            show="headings"   ,
            style="Custom.Treeview"     
        )

        for i, col in enumerate(self.columns):
            width = 120
            if column_widths and i < len(column_widths):
                width = column_widths[i]
            self.tree.column(col, width=width, anchor="center")
            self.tree.heading(col, text=col)

        
        # Inserir dados
        for row in self.data:
            self.tree.insert("", "end", values=row)

        # Scroolbar vertical
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _create_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        customed_style = ttk.Style()
        customed_style.configure('Custom.Treeview', highlightthickness=0, bd=0, font=('Helvetica', 10))
        customed_style.configure('Custom.Treeview.Heading', font=('Helvetica', 10, 'bold'), background="blue", foreground="white", relief="flat")

        style.map(
            "Custom.Treeview.Heading",
            background=[("active", "blue")],
            foreground=[("active", "white")]
        )
        style.map(
            "Custom.Treeview",
            background=[("selected", "#0d6efd")],
            foreground=[("selected", "white")]
        )