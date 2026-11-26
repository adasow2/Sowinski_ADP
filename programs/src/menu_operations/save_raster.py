from tkinter import filedialog, messagebox

from src.layers import state


def get_output(layer_name="raster"):
    return filedialog.asksaveasfilename(
        title="Zapisz raster",
        defaultextension=".tif",
        initialfile=f"{layer_name}.tif",
        filetypes=[
            ("Pliki rastrowe", "*.tif *.tiff *.img *.jp2"),
            ("Wszystkie pliki", "*.*"),
        ],
        confirmoverwrite=True,
    )


def save_raster(layer_id):
    if layer_id is None:
        return False

    raster = state.get_layer(layer_id)
    if raster is None:
        return False

    out_path = get_output(raster.name)
    if not out_path:
        return False

    try:
        raster.save(out_path)
        messagebox.showinfo("Sukces", f"Pomyślnie zapisano raster:\n{out_path}")
        return True
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się zapisać rastra:\n{e}")
        return False