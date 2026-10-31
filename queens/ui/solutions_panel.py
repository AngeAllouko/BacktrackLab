"""Scrollable gallery of mini boards, one per solution found so far. Click one to view it."""
import tkinter as tk
from tkinter import ttk

from queens.ui.theme import ACCENT, BOARD_DARK, BOARD_LIGHT, CARD, FONT, KIND_COLORS, MUTED

THUMB = 92
MAX_SHOWN = 80


def draw_mini_board(canvas, n, queens, size=THUMB):
    cs = size / n
    for r in range(n):
        for c in range(n):
            canvas.create_rectangle(c * cs, r * cs, (c + 1) * cs, (r + 1) * cs,
                                    fill=BOARD_DARK if (r + c) % 2 else BOARD_LIGHT, outline="")
    rad = cs * 0.34
    for r, c in enumerate(queens):
        cx, cy = (c + .5) * cs, (r + .5) * cs
        canvas.create_oval(cx - rad, cy - rad, cx + rad, cy + rad, fill=KIND_COLORS["solution"], outline="")


class SolutionsPanel(ttk.Frame):
    def __init__(self, parent, on_select):
        super().__init__(parent, style="Card.TFrame")
        self._on_select = on_select
        self._count = -1
        self._n = 0
        self._canvas = tk.Canvas(self, bg=CARD, highlightthickness=0)
        scroll = ttk.Scrollbar(self, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)
        self._inner = ttk.Frame(self._canvas, style="Card.TFrame")
        self._canvas.create_window((0, 0), window=self._inner, anchor="nw")
        self._inner.bind("<Configure>", lambda _e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))

    def set_solutions(self, solutions, n):
        """Rebuild the gallery only when the number of solutions (or N) changed."""
        if len(solutions) == self._count and n == self._n:
            return
        self._count, self._n = len(solutions), n
        for child in self._inner.winfo_children():
            child.destroy()
        if not solutions:
            ttk.Label(self._inner, text="No solution found yet.\nPress Next solution ⏭ to jump to one.",
                      style="Muted.TLabel", justify="left").grid(padx=8, pady=8)
            return
        per_row = 3
        for i, event in enumerate(solutions[:MAX_SHOWN]):
            cell = ttk.Frame(self._inner, style="Card.TFrame")
            cell.grid(row=i // per_row, column=i % per_row, padx=6, pady=6)
            thumb = tk.Canvas(cell, width=THUMB, height=THUMB, highlightthickness=1,
                              highlightbackground=ACCENT, cursor="hand2")
            thumb.pack()
            draw_mini_board(thumb, n, event["queens"])
            thumb.bind("<Button-1>", lambda _e, k=i: self._on_select(k))
            ttk.Label(cell, text=f"#{i + 1}", style="Muted.TLabel").pack()
        if len(solutions) > MAX_SHOWN:
            ttk.Label(self._inner, text=f"... and {len(solutions) - MAX_SHOWN} more",
                      style="Muted.TLabel").grid(row=99, column=0, columnspan=3, pady=6)
