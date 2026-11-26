from src.layers.raster import RasterLayer
from tkinter import filedialog, messagebox

# Globalna lista otwartych okien warstw lub funkcji odświeżania
active_layer_windows = []

def register_layer_window(window_refresh_callback):
    if window_refresh_callback not in active_layer_windows:
        active_layer_windows.append(window_refresh_callback)

def unregister_layer_window(window_refresh_callback):
    if window_refresh_callback in active_layer_windows:
        active_layer_windows.remove(window_refresh_callback)

def read_raster():
    path = filedialog.askopenfilename(
        title="Wybierz raster",
        filetypes=[
            ("Pliki rastrowe", "*.tif *.tiff *.img *.jp2"),
            ("Wszystkie pliki", "*.*")
        ],
    )
    if not path:
        return None

    try:
        RasterLayer.read_raster(path)
        # Automatyczne odświeżenie wszystkich otwartych okien tabeli warstw
        for callback in list(active_layer_windows):
            try:
                callback()
            except Exception:
                active_layer_windows.remove(callback)
        messagebox.showinfo("Sukces", f"Pomyślnie wczytano raster:\n{path}")
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się wczytać rastra:\n{e}")
