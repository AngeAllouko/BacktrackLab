"""Draws the chessboard for one event. Pure drawing: it never changes any state."""
from queens.rules import attacked_squares
from queens.ui.theme import (ATTACK_DARK, ATTACK_LIGHT, BOARD_DARK, BOARD_LIGHT, BG, FONT,
                             KIND_COLORS, KIND_TINTS, MUTED, QUEEN_FILL)

MARGIN = 34


class BoardView:
    def __init__(self, canvas):
        self.canvas = canvas

    def render(self, n, event, show_attacks=True):
        cv = self.canvas
        cv.delete("all")
        W, H = cv.winfo_width(), cv.winfo_height()
        size = min(W, H) - 2 * MARGIN
        if size < 60:
            return
        cs = size / n
        x0, y0 = (W - size) / 2, (H - size) / 2

        queens = event["queens"] if event else []
        kind = event["kind"] if event else None
        cell = event.get("cell") if event else None
        attacked = attacked_squares(queens, n) if show_attacks else set()

        def box(r, c):
            return x0 + c * cs, y0 + r * cs, x0 + (c + 1) * cs, y0 + (r + 1) * cs

        def center(r, c):
            return x0 + (c + .5) * cs, y0 + (r + .5) * cs

        # squares (red-tinted when attacked by a placed queen)
        for r in range(n):
            for c in range(n):
                dark = (r + c) % 2 == 1
                if (r, c) in attacked:
                    fill = ATTACK_DARK if dark else ATTACK_LIGHT
                else:
                    fill = BOARD_DARK if dark else BOARD_LIGHT
                cv.create_rectangle(*box(r, c), fill=fill, outline="")

        # coordinates
        for i in range(n):
            cv.create_text(x0 + (i + .5) * cs, y0 - 14, text=str(i), fill=MUTED, font=(FONT, 10))
            cv.create_text(x0 - 16, y0 + (i + .5) * cs, text=str(i), fill=MUTED, font=(FONT, 10))

        # candidate square
        if cell:
            r, c = cell
            ring = KIND_COLORS[kind]
            cv.create_rectangle(*box(r, c), fill=KIND_TINTS[kind], outline=ring, width=4)
        if cell and "conflict" in event:
            cv.create_line(*center(*event["conflict"]), *center(*cell), fill=KIND_COLORS["reject"],
                           width=4, dash=(8, 5), arrow="last", arrowshape=(14, 16, 6))

        # queens
        rad = cs * 0.36
        glyph = max(10, int(cs * 0.42))
        solved = kind == "solution"
        for r, c in enumerate(queens):
            cx, cy = center(r, c)
            hit = "conflict" in event and event["conflict"] == (r, c)
            cv.create_oval(cx - rad, cy - rad, cx + rad, cy + rad,
                           fill=KIND_COLORS["solution"] if solved else QUEEN_FILL,
                           outline=KIND_COLORS["reject"] if hit else "white", width=4 if hit else 2)
            cv.create_text(cx, cy, text="♛", fill="white", font=("Segoe UI Symbol", glyph))

        # symbol on the candidate square
        if cell and kind in ("try", "reject", "backtrack"):
            cx, cy = center(*cell)
            symbol = {"try": "?", "reject": "✕", "backtrack": "↩"}[kind]
            cv.create_text(cx, cy, text=symbol, fill=KIND_COLORS[kind] if kind != "try" else "#92400e",
                           font=(FONT, max(12, int(cs * 0.5)), "bold"))

        cv.create_rectangle(x0, y0, x0 + size, y0 + size, outline="#475569", width=2)
