"""'What is happening now?' card: colored badge, message and a plain-English explanation."""
import tkinter as tk
from tkinter import ttk

from queens.theory import KIND_EXPLANATIONS, KIND_LABELS
from queens.ui.card import Card
from queens.ui.theme import CARD, FONT, KIND_COLORS, MUTED, TEXT


class StepPanel(Card):
    def __init__(self, parent):
        super().__init__(parent, "What is happening?")
        self._badge = tk.Label(self.body, text="READY", bg="#9ca3af", fg="white",
                               font=(FONT, 10, "bold"), padx=12, pady=3)
        self._badge.pack(anchor="w")
        self._msg = tk.Label(self.body, bg=CARD, fg=TEXT, font=(FONT, 12, "bold"),
                             wraplength=340, justify="left", anchor="w")
        self._msg.pack(fill="x", pady=(8, 2))
        self._why = tk.Label(self.body, bg=CARD, fg=MUTED, font=(FONT, 10),
                             wraplength=340, justify="left", anchor="w")
        self._why.pack(fill="x")
        self._state = tk.Label(self.body, bg=CARD, fg=TEXT, font=("Consolas", 10), anchor="w")
        self._state.pack(fill="x", pady=(8, 0))
        self.show_idle()

    def show_idle(self, text="Press ▶ Play, or Step ▶ to go one decision at a time."):
        self._badge.config(text="READY", bg="#9ca3af")
        self._msg.config(text=text)
        self._why.config(text="Keyboard: Space = play/pause, ← → = back/step, N = next solution, R = reset.")
        self._state.config(text="queens = []")

    def show(self, event, prefix=""):
        kind = event["kind"]
        self._badge.config(text=KIND_LABELS[kind], bg=KIND_COLORS[kind])
        self._msg.config(text=prefix + event["msg"])
        self._why.config(text=KIND_EXPLANATIONS[kind])
        self._state.config(text=f"queens = {event['queens']}   depth = {len(event['queens'])}")

    def show_done(self, summary):
        self._badge.config(text="FINISHED", bg="#6366f1")
        self._msg.config(text=summary)
        self._why.config(text="Use ◀ Back to replay the search, or ↺ Reset to start again.")
