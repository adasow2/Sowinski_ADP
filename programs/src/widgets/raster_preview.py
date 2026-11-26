import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")
import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk,
)
from matplotlib.figure import Figure

_PLACEHOLDER = "Wybierz raster z tabeli, aby zobaczyć podgląd."


class RasterPreview(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=6)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()

        self.toolbar = NavigationToolbar2Tk(
            self.canvas, self, pack_toolbar=False
        )
        self.toolbar.update()

        self.placeholder = ttk.Label(
            self,
            text=_PLACEHOLDER,
            anchor="center",
            justify="center",
        )

        self._ax = None
        self._empty = True
        self.placeholder.pack(fill="both", expand=True)

        self.canvas.mpl_connect("scroll_event", self._on_scroll)

    def _show_canvas(self):
        if self._empty:
            self.placeholder.pack_forget()
            self.toolbar.pack(side="bottom", fill="x")
            self.canvas_widget.pack(side="top", fill="both", expand=True)
            self._empty = False

    def clear(self):
        self.figure.clear()
        self._ax = None
        self.canvas.draw_idle()

        if not self._empty:
            self.canvas_widget.pack_forget()
            self.toolbar.pack_forget()
            self.placeholder.pack(fill="both", expand=True)
            self._empty = True

    def show(self, layer):
        if layer is None:
            self.clear()
            return

        arr = layer.array
        layer_norm = arr / arr.max() * 255
        layer_norm = layer_norm.astype(np.uint8)

        self.figure.clear()
        self._ax = self.figure.add_subplot(111)
        self._ax.imshow(layer_norm, aspect="equal", interpolation="nearest")
        self._ax.set_axis_off()
        self.figure.tight_layout(pad=0)
        self._show_canvas()
        self.canvas.draw_idle()

    def _on_scroll(self, event):
        if self._ax is None or event.inaxes != self._ax:
            return

        if event.xdata is None or event.ydata is None:
            return

        scale = 1.2 if event.button == "up" else 1.0 / 1.2

        xlim = self._ax.get_xlim()
        ylim = self._ax.get_ylim()
        x_span = xlim[1] - xlim[0]
        y_span = ylim[1] - ylim[0]

        rel_x = (event.xdata - xlim[0]) / x_span
        rel_y = (event.ydata - ylim[0]) / y_span

        new_span_x = x_span / scale
        new_span_y = y_span / scale

        self._ax.set_xlim(
            event.xdata - new_span_x * rel_x,
            event.xdata + new_span_x * (1.0 - rel_x),
        )
        self._ax.set_ylim(
            event.ydata - new_span_y * rel_y,
            event.ydata + new_span_y * (1.0 - rel_y),
        )
        self.canvas.draw_idle()