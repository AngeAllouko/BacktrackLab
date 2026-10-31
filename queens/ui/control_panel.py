"""Controls card: board size, options, Back / Play / Step buttons, speed."""
import tkinter as tk
from tkinter import ttk

from queens.ui.card import Card

MAX_N = 10


class ControlPanel(Card):
    """callbacks: on_change, on_back, on_play, on_step, on_next, on_reset, on_toggle_attacks"""

    def __init__(self, parent, cb):
        super().__init__(parent, "Controls")
        b = self.body
        b.columnconfigure((0, 1, 2), weight=1, uniform="btn")

        top = ttk.Frame(b, style="Card.TFrame")
        top.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 8))
        ttk.Label(top, text="Board size  N =", style="Card.TLabel").pack(side="left")
        self._n_var = tk.StringVar(value="6")
        self._last_n = 6
        spin = ttk.Spinbox(top, from_=1, to=MAX_N, width=4, textvariable=self._n_var, command=cb["on_change"])
        spin.pack(side="left", padx=8)
        spin.bind("<Return>", lambda _e: cb["on_change"]())
        spin.bind("<FocusOut>", lambda _e: cb["on_change"]())
        self.spinbox = spin

        self._find_all = tk.BooleanVar(value=False)
        ttk.Checkbutton(b, text="Find all solutions (don't stop at the first)", style="Card.TCheckbutton",
                        variable=self._find_all, command=cb["on_change"]).grid(
            row=1, column=0, columnspan=3, sticky="w")
        self._attacks = tk.BooleanVar(value=True)
        ttk.Checkbutton(b, text="Shade attacked squares", style="Card.TCheckbutton",
                        variable=self._attacks, command=cb["on_toggle_attacks"]).grid(
            row=2, column=0, columnspan=3, sticky="w", pady=(2, 8))

        ttk.Button(b, text="◀ Back", command=cb["on_back"]).grid(row=3, column=0, sticky="ew", padx=(0, 3))
        self._play = ttk.Button(b, text="▶ Play", style="Accent.TButton", command=cb["on_play"])
        self._play.grid(row=3, column=1, sticky="ew", padx=3)
        ttk.Button(b, text="Step ▶", command=cb["on_step"]).grid(row=3, column=2, sticky="ew", padx=(3, 0))
        ttk.Button(b, text="⏭ Next solution", command=cb["on_next"]).grid(
            row=4, column=0, columnspan=2, sticky="ew", pady=(6, 0), padx=(0, 3))
        ttk.Button(b, text="↺ Reset", command=cb["on_reset"]).grid(row=4, column=2, sticky="ew", pady=(6, 0), padx=(3, 0))

        speed = ttk.Frame(b, style="Card.TFrame")
        speed.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(10, 0))
        ttk.Label(speed, text="Speed", style="Card.TLabel").pack(side="left")
        self._speed = tk.IntVar(value=5)
        self._speed_lbl = ttk.Label(speed, text="5 steps/s", style="Muted.TLabel", width=11, anchor="e")
        self._speed_lbl.pack(side="right")
        ttk.Scale(speed, from_=1, to=60, variable=self._speed, style="Card.Horizontal.TScale",
                  command=lambda _v: self._speed_lbl.config(text=f"{self._speed.get()} steps/s")).pack(
            side="left", fill="x", expand=True, padx=8)

    @property
    def n(self):
        try:
            value = int(self._n_var.get())
        except ValueError:
            value = self._last_n
        value = max(1, min(MAX_N, value))
        self._n_var.set(str(value))
        self._last_n = value
        return value

    @property
    def find_all(self):
        return self._find_all.get()

    @property
    def show_attacks(self):
        return self._attacks.get()

    @property
    def delay_ms(self):
        return max(10, int(1000 / max(1, self._speed.get())))

    def set_playing(self, playing):
        self._play.config(text="⏸ Pause" if playing else "▶ Play")
