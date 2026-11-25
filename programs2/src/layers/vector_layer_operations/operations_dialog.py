import tkinter as tk
from tkinter import ttk

class SimpleOperationsDialog(tk.Toplevel):
    def __init__(self, parent, layer_id, layer_obj, callback_refresh):
        super().__init__(parent)
        self.title("Operacje")
        self.geometry("300x150")
        lbl = ttk.Label(self, text="Operacje dla rastrów")
        lbl.pack(pady=20)
