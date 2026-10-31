# N-Queens by Backtracking — Viva Cheat-Sheet

## 1. The 60-second answer
> "Backtracking builds a solution one decision at a time and **abandons a partial solution as soon as it
> cannot possibly lead to a valid answer**. For N-Queens I place one queen per row. For each row I try the
> columns left to right; if a square is attacked I **reject** it (prune), otherwise I **place** the queen and
> recurse to the next row. If a row has no safe column, I **backtrack**: remove the previous queen and try its
> next column. When all N rows are filled, I have a solution."

Backtracking = **depth-first search of the state-space tree + a feasibility check (pruning)**.

## 2. The rule (file `queens/rules.py`)
Queens at (r1,c1) and (r2,c2) attack each other if
* same column: `c1 == c2`, or
* same diagonal: `|c1 - c2| == |r1 - r2|`.

Same row can never happen, because we place exactly one queen per row.

## 3. The algorithm (file `queens/algorithm.py`)
```
place_row(r):
    if r == N:  record solution; return
    for c in 0..N-1:
        if safe(r, c):          # no attacker in earlier rows
            cols.append(c)      # CHOOSE
            place_row(r + 1)    # EXPLORE
            cols.pop()          # UNDO  <-- this line IS the backtracking
        # else: PRUNE (skip)
```
`cols[r]` = column of the queen in row r. That list is the *partial solution* / the current path in the tree.

**Choose → Explore → Undo** is the template for every backtracking problem.

## 4. State-space tree
* Root = empty board. Level r = "which column for row r" (N children each).
* A node is **promising** if no two queens so far attack each other. Non-promising nodes are pruned.
* Without pruning the tree has N^N leaves; with pruning we only visit promising nodes.
* Measured with this app, N = 8: the whole search (all 92 solutions) places 2,056 queens, i.e. about
  2,057 tree nodes including the root, versus 16,777,216 boards for brute force and 40,320 permutations.

## 5. Complexity
| | Value | Why |
|---|---|---|
| Time | **O(N!)** | row 0 has ≤N choices, row 1 ≤N−1 (column taken), ... so at most N! full paths. The safety check costs O(N) per square, so a strict bound is O(N·N!). Pruning makes real runs much smaller. |
| Space | **O(N)** | recursion depth N + the `cols` list of N numbers. |
| (This app only) | O(steps) | it stores the event history so ◀ Back works. That is visualisation overhead, not part of the algorithm. |

Number of solutions: N=1→1, 2→0, 3→0, 4→2, 5→10, 6→4, 7→40, 8→92, 9→352, 10→724.

## 6. Likely viva questions (with short answers)
1. **What is backtracking?** Systematic DFS of the solution space that undoes a choice when it leads to a dead end.
2. **Backtracking vs brute force?** Brute force generates every full candidate then checks it; backtracking checks constraints at every step and prunes whole subtrees early.
3. **Explicit vs implicit constraints?** Explicit: each queen's column is in 0..N−1 (one per row). Implicit: no two queens share a column or diagonal.
4. **Bounding / feasibility function here?** `attacker()` — "is this square attacked by an earlier queen?"
5. **Why one queen per row?** Two queens in a row always attack, so it loses nothing and shrinks the search from choosing N squares out of N² to N^N.
6. **Why do N=2 and N=3 have no solution?** Every placement of the 1st and 2nd queens blocks all squares of the next row; the app shows this (try N=3).
7. **Is backtracking DFS or BFS?** DFS (recursion = the stack).
8. **How could it be faster?** Keep sets/bitmasks of used columns and diagonals (`r−c`, `r+c`) for an O(1) check; use symmetry (only search the left half of row 0 and mirror).
9. **Backtracking vs branch and bound?** Backtracking finds feasible/all solutions; branch and bound optimises a cost and prunes using bounds.
10. **Which line is the backtrack?** `cols.pop()` after `yield from place_row(r + 1)`.
11. **Why is the algorithm a generator?** Each `yield` hands one decision to the UI, so the GUI can animate or step it without the algorithm knowing about Tkinter.
12. **How many solutions for N=8, and how many are "really different"?** 92; 12 distinct if rotations and reflections are treated as the same.
13. **Worst-case example of a non-pruned branch?** Any square in an attacked row/column/diagonal: shown red with ✕ in the app.

## 7. Map of the code (each file has ONE job)
| File | Job |
|---|---|
| `queens/rules.py` | the attack rule |
| `queens/algorithm.py` | the backtracking algorithm (yields events) |
| `queens/session.py` | records events; Step forward / Back; statistics |
| `queens/playback.py` | Play and Next-solution timing |
| `queens/theory.py` | explanation texts + complexity numbers |
| `queens/ui/board_view.py` | draws the board |
| `queens/ui/*_panel.py`, `card.py`, `board_card.py` | the interface panels |
| `queens/ui/app.py` | builds the window and connects everything |

**One click, traced:** Step ▶ → `App.step` → `Playback.step` → `Session.forward` → next event from
`solve_nqueens` → `App.refresh` → `BoardView.render` + panels update.

## 8. Demo script (5 minutes)
1. **N = 4, Step ▶** one by one. Point out *trying → rejected (red arrow shows the attacker) → placed → backtrack*. The first solution `[1, 3, 0, 2]` appears after 57 steps (8 placements, 18 rejections, 4 backtracks).
2. Press **◀ Back** to show you can replay a decision. Toggle **Shade attacked squares**.
3. **N = 3** → search ends with "no solution".
4. **N = 8, Find all, Next solution ⏭** → 92 solutions (gallery + counters). Open the **Complexity** tab.
5. Say: "The `cols.pop()` line is the backtracking; the red ✕ is the pruning."

## 9. Three-day plan
* **Day 1 – theory:** sections 1–5. Solve N=4 on paper (you should get `[1,3,0,2]` and `[2,0,3,1]`). Draw the 4-queens state-space tree.
* **Day 2 – code:** read `rules.py`, `algorithm.py`, `session.py` in that order; run `python -m unittest discover -s tests -t .`; change something small (e.g. try columns from right to left and watch the first solution change).
* **Day 3 – rehearse:** run the demo script out loud; answer section 6 without looking; be ready to explain one UI file.
