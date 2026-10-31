"""Complexity analysis text (updates when N changes)."""
from tkinter import ttk

from queens.theory import complexity_text


class TheoryPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame", padding=12)
        self._label = ttk.Label(self, style="Card.TLabel", justify="left", wraplength=340)
        self._label.pack(anchor="w")

    def show(self, n):
        self._label.config(text=complexity_text(n))
