import tkinter as tk
from tkinter import ttk
from ..state import layers_table, layers_dict

class LayerTableWidget(ttk.Frame):
    def __init__(self, parent, col_widths=None):
        super().__init__(parent)

        if col_widths is None:
            col_widths = {
                "nazwa": 150,
                "wysokość": 100,
                "szerokość": 100,
                "crs": 150,
                "liczba kanałów": 110
            }

        self.col_widths = col_widths
        self.columns = list(col_widths.keys())

        self.create_widgets()
        self.load_layers()

    def create_widgets(self):
        self.frame_table = ttk.Frame(self)
        self.frame_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.frame_table, columns=self.columns, show="headings")
        for col, width in self.col_widths.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="w")

        scrollbar = ttk.Scrollbar(self.frame_table, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def load_layers(self):
        """Odświeża listę warstw rastrowych z obiektu stanu layers_table / layers_dict."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for idx, row in layers_table.iterrows():
            self.tree.insert("", tk.END, iid=str(idx), values=(
                row.get("nazwa"),
                row.get("wysokość"),
                row.get("szerokość"),
                row.get("crs"),
                row.get("liczba kanałów")
            ))

    def get_selected_layer_ids(self):
        return self.tree.selection()
