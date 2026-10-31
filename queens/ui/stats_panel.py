"""Five live counters shown as tiles."""
from tkinter import ttk

from queens.ui.card import Card

TILES = [("steps", "Steps"), ("depth", "Depth"), ("rejects", "Rejections"),
         ("backtracks", "Backtracks"), ("solutions", "Solutions")]


class StatsPanel(Card):
    def __init__(self, parent):
        super().__init__(parent)
        self._values = {}
        for col, (key, caption) in enumerate(TILES):
            self.body.columnconfigure(col, weight=1)
            cell = ttk.Frame(self.body, style="Card.TFrame")
            cell.grid(row=0, column=col, sticky="ew")
            value = ttk.Label(cell, text="0", style="Tile.TLabel", anchor="center")
            value.pack(fill="x")
            ttk.Label(cell, text=caption, style="TileCaption.TLabel", anchor="center").pack(fill="x")
            self._values[key] = value

    def show(self, stats, depth):
        data = dict(stats, depth=depth)
        for key, label in self._values.items():
            label.config(text=str(data[key]))
