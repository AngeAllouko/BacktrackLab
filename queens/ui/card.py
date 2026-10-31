"""A white rounded-looking panel with a title - the building block of the layout."""
import tkinter as tk
from tkinter import ttk

from queens.ui.theme import BORDER, CARD, FONT, TEXT


class Card(tk.Frame):
    def __init__(self, parent, title=None):
        super().__init__(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        if title:
            tk.Label(self, text=title, bg=CARD, fg=TEXT, font=(FONT, 11, "bold"),
                     anchor="w").pack(fill="x", padx=14, pady=(10, 2))
        self.body = ttk.Frame(self, style="Card.TFrame", padding=(14, 6, 14, 12))
        self.body.pack(fill="both", expand=True)
