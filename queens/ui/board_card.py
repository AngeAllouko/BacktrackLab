"""The big card that holds the board canvas and the color legend."""
import tkinter as tk
from tkinter import ttk

from queens.theory import KIND_LABELS
from queens.ui.board_view import BoardView
from queens.ui.card import Card
from queens.ui.theme import BG, CARD, KIND_COLORS


class BoardCard(Card):
    def __init__(self, parent, on_resize):
        super().__init__(parent)
        self.canvas = tk.Canvas(self.body, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=8, pady=(8, 0))
        self.canvas.bind("<Configure>", lambda _e: on_resize())
        self.view = BoardView(self.canvas)

        legend = ttk.Frame(self.body, style="Card.TFrame")
        legend.pack(fill="x", padx=14, pady=10)
        for kind, label in KIND_LABELS.items():
            tk.Label(legend, bg=KIND_COLORS[kind], width=2).pack(side="left", padx=(0, 5))
            ttk.Label(legend, text=label.capitalize(), style="Card.TLabel").pack(side="left", padx=(0, 16))
