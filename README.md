# BacktrackLab - N-Queens

A Tkinter desktop app that visualises how **backtracking** solves the N-Queens problem
(MCA - Design & Analysis of Algorithms, Unit 3).

## Run
    python main.py                                   # Python 3.8+, Tkinter included
    python -m unittest discover -s tests -t .        # tests

## Using it
* Choose **N** (1-10). Press **Play**, or go one decision at a time with **Step** / **Back**.
* **Next solution** jumps to the next valid arrangement. Tick **Find all solutions** to keep going.
* Colors: yellow = trying, green = placed, red = rejected (pruned), orange = backtrack, blue = solution.
* Red-shaded squares are attacked by queens already placed.
* Click a mini board in the **Solutions** tab to view it. The **Complexity** tab shows the numbers for your N.
* Keys: Space play/pause, Left/Right back/step, N next solution, R reset.

## Layout (one job per file)
    main.py                 entry point
    queens/
      rules.py              the attack rule
      algorithm.py          backtracking algorithm (generator of events)
      session.py            event history, step forward/back, statistics
      playback.py           Play / Next-solution timing
      theory.py             explanation texts and complexity numbers
      ui/
        theme.py            colors, fonts, ttk styles
        card.py             titled panel used everywhere
        board_view.py       draws the board
        board_card.py       board canvas + legend
        control_panel.py    N, options, buttons, speed
        step_panel.py       "what is happening?" badge and explanation
        stats_panel.py      live counters
        solutions_panel.py  gallery of solutions
        theory_panel.py     complexity text
        app.py              main window, wires everything together
    tests/                  headless unit tests
