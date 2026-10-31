"""A search in progress: records every event so we can step forward AND backward."""

EMPTY_STATS = {"steps": 0, "rejects": 0, "backtracks": 0, "solutions": 0}


class Session:
    def __init__(self, generator):
        self._gen = generator
        self._history = []            # list of (event, stats-after-this-event)
        self._solutions = []
        self._stats = dict(EMPTY_STATS)
        self.cursor = -1              # index of the event being shown (-1 = empty board)
        self.exhausted = False        # the generator has no more events

    @property
    def current(self):
        """(event, stats) at the cursor; (None, zero stats) before the first step."""
        if self.cursor < 0:
            return None, dict(EMPTY_STATS)
        return self._history[self.cursor]

    def forward(self):
        """Move one step forward. Returns the event, or None when the search is over."""
        if self.cursor + 1 < len(self._history):          # replay something we already computed
            self.cursor += 1
            return self._history[self.cursor][0]
        if self.exhausted:
            return None
        try:
            event = next(self._gen)
        except StopIteration:
            self.exhausted = True
            return None
        self._stats["steps"] += 1
        if event["kind"] == "reject":
            self._stats["rejects"] += 1
        elif event["kind"] == "backtrack":
            self._stats["backtracks"] += 1
        elif event["kind"] == "solution":
            self._stats["solutions"] += 1
            self._solutions.append(event)
        self._history.append((event, dict(self._stats)))
        self.cursor += 1
        return event

    def back(self):
        """Move one step back. Returns False if already at the empty board."""
        if self.cursor < 0:
            return False
        self.cursor -= 1
        return True

    def solutions_so_far(self):
        """Solutions found up to the cursor (so stepping back 'un-finds' them)."""
        return self._solutions[: self.current[1]["solutions"]]

    def summary(self, n):
        found = self._stats["solutions"]
        if found:
            return f"Search complete: {found} solution(s) found for N = {n}."
        return f"Search complete: no solution exists for N = {n}."
