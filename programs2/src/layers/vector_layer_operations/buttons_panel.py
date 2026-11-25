import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
import numpy as np
from ..state import layers_dict, layers_table
from ..raster import RasterLayer
from .table import LayerTableWidget

class LayerButtonsPanel(ttk.Frame):
    def __init__(self, parent, table_widget: LayerTableWidget):
        super().__init__(parent, padding=10)
        self.table_widget = table_widget
        self.parent_window = parent

        # Przycisk wczytywania warstwy rastrowej
        btn_load = ttk.Button(
            self,
            text="Wczytaj raster",
            command=self.load_data
        )
        btn_load.pack(fill=tk.X, pady=5)

        # Przycisk do wyświetlania rastra
        btn_show = ttk.Button(
            self,
            text="Pokaż zaznaczony raster",
            command=self.plot_selected_layers
        )
        btn_show.pack(fill=tk.X, pady=5)

        # Przycisk usuwania
        btn_remove = ttk.Button(
            self,
            text="Usuń zaznaczone",
            command=self.remove_selected_layers
        )
        btn_remove.pack(fill=tk.X, pady=5)

        # Przycisk zapisu
        btn_save = ttk.Button(
            self,
            text="Zapisz zaznaczony raster",
            command=self.save_selected_layer
        )
        btn_save.pack(fill=tk.X, pady=5)

    def load_data(self):
        path = filedialog.askopenfilename(
            title='Wybierz raster',
            filetypes=[("GeoTIFF / Raster", "*.tif *.tiff *.img"), ("Wszystkie pliki", "*.*")]
        )
        if not path:
            return

        try:
            RasterLayer.read_raster(path)
            self.table_widget.load_layers()
        except Exception as e:
            messagebox.showwarning(
                "Błąd wczytywania",
                f"Nie udało się wczytać wybranego rastra:\n{e}"
            )

    def plot_selected_layers(self):
        selected_items = self.table_widget.get_selected_layer_ids()
        if not selected_items:
            return

        for item_id in selected_items:
            idx = int(item_id)
            if idx < len(layers_table):
                row = layers_table.iloc[idx]
                layer_name = row["nazwa"]
                if layer_name in layers_dict:
                    raster_obj = layers_dict[layer_name]
                    arr = raster_obj.array
                    fig, ax = plt.subplots(figsize=(8, 8))
                    ax.set_title(f"Raster: {layer_name}")
                    
                    if arr.shape[2] >= 3:
                        # RGB
                        disp_arr = arr[:, :, :3]
                        # normalizacja do 0-1 lub 0-255 jeśli trzeba
                        if disp_arr.dtype != np.uint8:
                            d_min, d_max = disp_arr.min(), disp_arr.max()
                            if d_max > d_min:
                                disp_arr = (disp_arr - d_min) / (d_max - d_min)
                        ax.imshow(disp_arr)
                    elif arr.shape[2] == 1:
                        ax.imshow(arr[:, :, 0], cmap='gray')
                    else:
                        ax.imshow(arr[:, :, 0], cmap='viridis')

                    plt.tight_layout()
                    plt.show()

    def remove_selected_layers(self):
        selected_items = self.table_widget.get_selected_layer_ids()
        if not selected_items:
            return

        # Usuwamy od tyłu żeby indeksy się nie rozjechały
        indices_to_remove = sorted([int(item_id) for item_id in selected_items], reverse=True)
        for idx in indices_to_remove:
            if idx < len(layers_table):
                row_name = layers_table.iloc[idx]["nazwa"]
                if row_name in layers_dict:
                    del layers_dict[row_name]
                layers_table.drop(index=idx, inplace=True)
        
        layers_table.reset_index(drop=True, inplace=True)
        self.table_widget.load_layers()

    def save_selected_layer(self):
        selected_items = self.table_widget.get_selected_layer_ids()
        if not selected_items:
            messagebox.showwarning("Brak zaznaczenia", "Zaznacz raster do zapisu.")
            return

        if len(selected_items) > 1:
            messagebox.showwarning("Zbyt wiele zaznaczeń", "Wybierz tylko jeden raster do zapisu.")
            return

        idx = int(selected_items[0])
        if idx >= len(layers_table):
            return

        row = layers_table.iloc[idx]
        layer_name = row["nazwa"]
        if layer_name not in layers_dict:
            return

        raster_obj = layers_dict[layer_name]

        file_path = filedialog.asksaveasfilename(
            title="Zapisz raster jako",
            defaultextension=".tif",
            filetypes=[
                ("GeoTIFF", "*.tif"),
                ("Wszystkie pliki", "*.*")
            ]
        )

        if not file_path:
            return

        try:
            raster_obj.save(file_path)
            messagebox.showinfo("Sukces", f"Pomyślnie zapisano raster do:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Błąd zapisu", f"Nie udało się zapisać pliku:\n{e}")
