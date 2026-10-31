"""N-Queens by backtracking, written as a generator that yields one event per decision.

Event kinds:
    try        considering a column in the current row
    place      the square is safe -> keep the queen and go to the next row
    reject     the square is attacked -> prune (do not go deeper)
    backtrack  undo the queen after the deeper search is finished
    solution   all N queens are placed
"""
from queens.rules import attacker


def event(kind, msg, **state):
    return {"kind": kind, "msg": msg, **state}


def solve_nqueens(n, find_all):
    cols = []            # cols[r] = column of the queen in row r  (the current partial solution)
    stop = False

    def place_row(r):
        nonlocal stop
        if r == n:                                                        # base case: board full
            yield event("solution", f"Solution found: columns = {cols}", queens=list(cols))
            if not find_all:
                stop = True
            return
        for c in range(n):                                                # try every column
            if stop:
                return
            yield event("try", f"Row {r}: try column {c}", queens=list(cols), cell=(r, c))
            bad = attacker(cols, r, c)
            if bad is None:                                               # safe -> choose
                cols.append(c)
                yield event("place", f"Place queen at row {r}, column {c}", queens=list(cols), cell=(r, c))
                yield from place_row(r + 1)                               # explore deeper
                if stop:
                    return
                cols.pop()                                                # undo -> backtrack
                yield event("backtrack", f"Remove queen from row {r}, column {c} and try the next column",
                            queens=list(cols), cell=(r, c))
            else:                                                         # attacked -> prune
                yield event("reject", f"({r},{c}) is attacked by the queen at ({bad},{cols[bad]})",
                            queens=list(cols), cell=(r, c), conflict=(bad, cols[bad]))

    yield from place_row(0)
