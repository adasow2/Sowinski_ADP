import tkinter as tk

from src.layers import state
from src.menu_operations.close_program import close_program
from src.menu_operations.close_raster import close_raster
from src.menu_operations.read_raster import read_raster
from src.widgets.raster_preview import RasterPreview
from src.widgets.raster_table import RasterTablePanel
from src.widgets.toolbar import build_toolbar
from src.menu_operations.save_raster import save_raster

class KugisApp:
    def __init__(self, window: tk.Misc):
        self.window = window
        self._build_ui()

    def _build_ui(self):
        toolbar = build_toolbar(
            self.window,
            on_load=self.on_load,
            on_close_file=self.on_close_file,
            on_close_program=self.on_close_program,
            on_save_file=self.on_save_file
        )
        toolbar.pack(side="top", fill="x")

        body = tk.Frame(self.window)
        body.pack(side="top", fill="both", expand=True)

        self.table = RasterTablePanel(body, on_select=self.on_select)
        self.table.pack(side="left", fill="y")

        self.preview = RasterPreview(body)
        self.preview.pack(side="left", fill="both", expand=True)

    def on_load(self):
        read_raster()

    def on_close_file(self):
        layer_id = self.table.selected_id()
        if layer_id is None:
            return
        if close_raster(layer_id):
            self.table.refresh()
            self.preview.clear()

    def on_save_file(self):
        layer_id = self.table.selected_id()
        if layer_id is None:
            return
        if save_raster(layer_id):
            self.table.refresh()
            self.preview.clear()

    def on_close_program(self):
        close_program(self.window)

    def on_select(self, layer_id):
        layer = state.get_layer(layer_id) if layer_id is not None else None
        self.preview.show(layer)
