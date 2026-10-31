"""Colors, fonts and ttk styles. Change the look of the whole app here."""
from tkinter import ttk

FONT = "Segoe UI"
BG, CARD, BORDER = "#0a162c", "#ffffff", "#e2e6ee"
TEXT, MUTED, ACCENT, ACCENT_DARK = "#1f2937", "#6b7280", "#4f46e5", "#4338ca"

KIND_COLORS = {"try": "#f59e0b", "place": "#10b981", "reject": "#ef4444",
               "backtrack": "#f97316", "solution": "#3b82f6"}
KIND_TINTS = {"try": "#fde68a", "place": "#a7f3d0", "reject": "#fecaca",
              "backtrack": "#fed7aa", "solution": "#bfdbfe"}

BOARD_LIGHT, BOARD_DARK = "#eef2f7", "#8fa3bf"
ATTACK_LIGHT, ATTACK_DARK = "#f9d9dc", "#d98b94"
QUEEN_FILL = "#1e3a8a"


def apply_style(root):
    root.configure(bg=BG)
    s = ttk.Style(root)
    s.theme_use("clam")
    s.configure("TFrame", background=BG)
    s.configure("Card.TFrame", background=CARD)
    s.configure("Card.TLabel", background=CARD, foreground=TEXT, font=(FONT, 10))
    s.configure("Muted.TLabel", background=CARD, foreground=MUTED, font=(FONT, 9))
    s.configure("Tile.TLabel", background=CARD, foreground=TEXT, font=(FONT, 18, "bold"))
    s.configure("TileCaption.TLabel", background=CARD, foreground=MUTED, font=(FONT, 8))
    s.configure("TButton", font=(FONT, 10), padding=(10, 7), background="#e5e7eb",
                foreground=TEXT, borderwidth=0, focuscolor="#e5e7eb")
    s.map("TButton", background=[("active", "#d1d5db")])
    s.configure("Accent.TButton", background=ACCENT, foreground="white", font=(FONT, 10, "bold"))
    s.map("Accent.TButton", background=[("active", ACCENT_DARK)])
    s.configure("Card.TCheckbutton", background=CARD, foreground=TEXT, font=(FONT, 10))
    s.map("Card.TCheckbutton", background=[("active", CARD)])
    s.configure("Card.Horizontal.TScale", background=CARD)
    s.configure("TNotebook", background=BG, borderwidth=0)
    s.configure("TNotebook.Tab", padding=(14, 6), font=(FONT, 10))
