"""Main window: builds the layout and wires user actions to the Session and the panels."""
import tkinter as tk
from tkinter import ttk

from queens.algorithm import solve_nqueens
from queens.playback import Playback
from queens.session import Session
from queens.ui.board_card import BoardCard
from queens.ui.card import Card
from queens.ui.control_panel import ControlPanel
from queens.ui.solutions_panel import SolutionsPanel
from queens.ui.stats_panel import StatsPanel
from queens.ui.step_panel import StepPanel
from queens.ui.theme import ACCENT, FONT, apply_style
from queens.ui.theory_panel import TheoryPanel


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BacktrackLab - N-Queens")
        self.geometry("1320x820")
        self.minsize(1100, 740)
        apply_style(self)
        self.n = 0
        self.find_all = False
        self.session = None
        self.viewing = None            # a solution the user clicked in the gallery

        self._build_layout()
        self.playback = Playback(self, lambda: self.session.forward(), self._on_event, self._refresh_counters,
                                 self._on_finished, self.controls.set_playing, lambda: self.controls.delay_ms)
        self._bind_keys()
        self.new_session()

    # ---------------- layout ----------------
    def _build_layout(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        header = tk.Frame(self, bg=ACCENT)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        tk.Label(header, text="♛  BacktrackLab · N-Queens", bg=ACCENT, fg="white",
                 font=(FONT, 18, "bold")).pack(side="left", padx=20, pady=(12, 0))
        tk.Label(header, text="Watch backtracking try, prune and undo", bg=ACCENT, fg="#c7d2fe",
                 font=(FONT, 11)).pack(side="left", padx=8, pady=(18, 0))
        tk.Frame(header, height=12, bg=ACCENT).pack(side="bottom")

        self.board_card = BoardCard(self, on_resize=self.redraw)
        self.board_card.grid(row=1, column=0, sticky="nsew", padx=(16, 8), pady=16)

        right = ttk.Frame(self)
        right.grid(row=1, column=1, sticky="ns", padx=(8, 16), pady=16)
        self.controls = ControlPanel(right, {
            "on_change": self.on_settings_change, "on_back": self.back, "on_play": self.play,
            "on_step": self.step, "on_next": self.next_solution, "on_reset": self.new_session,
            "on_toggle_attacks": self.redraw})
        self.controls.pack(fill="x")
        self.step_panel = StepPanel(right)
        self.step_panel.pack(fill="x", pady=10)
        self.stats_panel = StatsPanel(right)
        self.stats_panel.pack(fill="x")

        tabs = ttk.Notebook(right)
        tabs.pack(fill="both", expand=True, pady=(10, 0))
        self.solutions_panel = SolutionsPanel(tabs, self.view_solution)
        self.theory_panel = TheoryPanel(tabs)
        tabs.add(self.solutions_panel, text="Solutions")
        tabs.add(self.theory_panel, text="Complexity")
        right.configure(width=400)
        right.pack_propagate(False)

    def _bind_keys(self):
        def on_key(action):
            def handler(_e):
                if isinstance(self.focus_get(), ttk.Spinbox):
                    return
                action()
            return handler
        self.bind("<space>", on_key(self.play))
        self.bind("<Right>", on_key(self.step))
        self.bind("<Left>", on_key(self.back))
        self.bind("<n>", on_key(self.next_solution))
        self.bind("<r>", on_key(self.new_session))

    # ---------------- session ----------------
    def new_session(self):
        self.playback.cancel()
        self.n = self.controls.n
        self.find_all = self.controls.find_all
        self.session = Session(solve_nqueens(self.n, self.find_all))
        self.viewing = None
        self.theory_panel.show(self.n)
        self.refresh()

    def on_settings_change(self):
        """N or 'find all' changed -> restart. (Ignore spurious focus events.)"""
        if self.controls.n != self.n or self.controls.find_all != self.find_all:
            self.new_session()

    # ---------------- user actions ----------------
    def step(self):
        self.viewing = None
        self.playback.cancel()
        self.playback.step()

    def back(self):
        self.viewing = None
        self.playback.cancel()
        self.session.back()
        self.refresh()

    def play(self):
        self.viewing = None
        self.playback.toggle_play()

    def next_solution(self):
        self.viewing = None
        self.playback.seek_solution()

    def view_solution(self, index):
        self.playback.cancel()
        self.viewing = self.session.solutions_so_far()[index]
        self.refresh()

    # ---------------- playback callbacks ----------------
    def _on_event(self, _event):
        self.refresh()

    def _on_finished(self):
        self._refresh_counters()
        self.step_panel.show_done(self.session.summary(self.n))

    # ---------------- rendering ----------------
    def refresh(self):
        self.redraw()
        event, _stats = self.session.current
        shown = self.viewing or event
        if shown is None:
            self.step_panel.show_idle()
        elif self.viewing:
            self.step_panel.show(shown, prefix="Viewing  ")
        else:
            self.step_panel.show(shown)
        self._refresh_counters()

    def _refresh_counters(self):
        event, stats = self.session.current
        self.stats_panel.show(stats, len(event["queens"]) if event else 0)
        self.solutions_panel.set_solutions(self.session.solutions_so_far(), self.n)

    def redraw(self):
        if self.session is None:
            return
        event, _ = self.session.current
        self.board_card.canvas.update_idletasks()
        self.board_card.view.render(self.n, self.viewing or event, self.controls.show_attacks)
