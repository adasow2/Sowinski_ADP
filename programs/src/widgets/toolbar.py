import tkinter as tk
from tkinter import ttk


def build_toolbar(parent, on_load, on_save_file, on_close_file, on_close_program):
    bar = ttk.Frame(parent, padding=(6, 4))

    menubtn = tk.Menubutton(bar, text="Plik", relief="raised", padx=8, pady=2)
    menu = tk.Menu(menubtn, tearoff=0)
    menu.add_command(label="Wczytaj raster", command=on_load)
    menu.add_command(label="Zamknij plik", command=on_close_file)
    menu.add_command(label="Zapisz plik", command=on_save_file)
    menubtn["menu"] = menu
    menubtn.pack(side="left")

    ttk.Button(bar, text="Zamknij program", command=on_close_program).pack(
        side="left", padx=(8, 0)
    )

    return bar
