"""The ONE rule of N-Queens: two queens attack if they share a column or a diagonal.

Rows never clash because we place exactly one queen per row.
"""


def attacker(cols, row, col):
    """Return the row of a queen that attacks (row, col), or None if the square is safe.

    cols[r] is the column of the queen already placed in row r.
    """
    for r, c in enumerate(cols):
        same_column = (c == col)
        same_diagonal = abs(c - col) == abs(r - row)
        if same_column or same_diagonal:
            return r
    return None


def attacked_squares(cols, n):
    """All squares below the placed queens that are attacked (used for the red shading)."""
    squares = set()
    for r, c in enumerate(cols):
        for rr in range(r + 1, n):
            d = rr - r
            for cc in (c, c - d, c + d):
                if 0 <= cc < n:
                    squares.add((rr, cc))
    return squares
