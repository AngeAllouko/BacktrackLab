"""Text and numbers for the explanation and complexity panels (no Tkinter)."""
from math import factorial

KIND_LABELS = {"try": "TRYING", "place": "PLACED", "reject": "REJECTED",
               "backtrack": "BACKTRACK", "solution": "SOLUTION"}

KIND_EXPLANATIONS = {
    "try": "The algorithm picks the next column of this row and tests it against the queens already placed.",
    "place": "The square is safe, so the queen is kept (CHOOSE) and the search moves to the next row (EXPLORE).",
    "reject": "A constraint is violated, so this branch is PRUNED: nothing below this square is ever explored.",
    "backtrack": "The deeper search is finished, so the last queen is removed (UNDO) and the next column is tried.",
    "solution": "Every row has a queen and no two attack each other: a complete valid arrangement.",
}

KNOWN_SOLUTIONS = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92, 9: 352, 10: 724}


def complexity_text(n):
    lines = [
        "Time complexity:   O(N!)",
        "Space complexity:  O(N)",
        "",
        f"For N = {n}:",
        f"  • Brute force (any squares): N^N = {n ** n:,} boards",
        f"  • One queen per row and column: N! = {factorial(n):,} permutations",
        "  • Backtracking cuts most of them off early (pruning).",
    ]
    if n in KNOWN_SOLUTIONS:
        lines.append(f"  • Number of valid solutions: {KNOWN_SOLUTIONS[n]}")
    return "\n".join(lines)
