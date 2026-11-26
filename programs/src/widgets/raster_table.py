import tkinter as tk
from tkinter import ttk

from src.layers import state
from src.menu_operations.read_raster import (
    register_layer_window,
    unregister_layer_window,
)

class RasterTablePanel(ttk.Frame):
    def __init__(self, parent, on_select=None):
        super().__init__(parent, padding=6)
        self.on_select = on_select
        self._cols = list(state.layers_table.columns)

        vsb = ttk.Scrollbar(self, orient="vertical")
        hsb = ttk.Scrollbar(self, orient="horizontal")

        self.tree = ttk.Treeview(
            self,
            columns=self._cols,
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
        )
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        for col in self._cols:
            self.tree.heading(col, text=str(col), anchor="w")
            self.tree.column(col, width=95, anchor="w", stretch=False)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        register_layer_window(self.refresh)
        self.refresh()

    def refresh(self):
        if not self.winfo_exists():
            return

        df = state.layers_table
        cols = list(df.columns)
        if cols != self._cols:
            self._cols = cols
            self.tree.configure(columns=cols)
            for col in cols:
                self.tree.heading(col, text=str(col), anchor="w")
                self.tree.column(col, width=95, anchor="w", stretch=False)

        self.tree.delete(*self.tree.get_children())
        for _, row in df.fillna("").iterrows():
            self.tree.insert("", "end", values=[row[col] for col in cols])

    def selected_id(self):
        selection = self.tree.selection()
        if not selection:
            return None
        values = self.tree.item(selection[0], "values")
        idx = self._cols.index("id")
        try:
            return int(values[idx])
        except (ValueError, TypeError):
            return None

    def _on_select(self, event=None):
        if self.on_select:
            self.on_select(self.selected_id())

    def destroy(self):
        unregister_layer_window(self.refresh)
        super().destroy()
