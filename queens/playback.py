"""Timing for Play and 'Next solution' (uses Tk's `after`; draws nothing itself)."""

SEEK_CHUNK = 3000        # events processed per timer tick while looking for a solution


class Playback:
    """
    advance()        -> next event, or None when finished
    on_event(event)  show it
    on_progress()    refresh counters only (used while seeking)
    on_finish()      the search is over
    on_state(bool)   playing flag changed (to update the Play/Pause button)
    delay_ms()       current delay between steps
    """

    def __init__(self, root, advance, on_event, on_progress, on_finish, on_state, delay_ms):
        self._root, self._advance = root, advance
        self._on_event, self._on_progress = on_event, on_progress
        self._on_finish, self._on_state = on_finish, on_state
        self._delay_ms = delay_ms
        self._after_id = None
        self.playing = False
        self.seeking = False

    def cancel(self):
        self.playing = self.seeking = False
        if self._after_id is not None:
            self._root.after_cancel(self._after_id)
            self._after_id = None
        self._on_state(False)

    def step(self):
        event = self._advance()
        if event is None:
            self._on_finish()
            return False
        self._on_event(event)
        return True

    def toggle_play(self):
        if self.playing:
            self.cancel()
            return
        self.playing = True
        self._on_state(True)
        self._tick()

    def seek_solution(self):
        self.cancel()
        self.seeking = True
        self._seek()

    def _tick(self):
        if not self.playing:
            return
        if not self.step():
            self.cancel()
            return
        self._after_id = self._root.after(self._delay_ms(), self._tick)

    def _seek(self):
        if not self.seeking:
            return
        event = None
        for _ in range(SEEK_CHUNK):
            event = self._advance()
            if event is None or event["kind"] == "solution":
                break
        if event is None:
            self.seeking = False
            self._on_progress()
            self._on_finish()
        elif event["kind"] == "solution":
            self.seeking = False
            self._on_event(event)
        else:
            self._on_progress()
            self._after_id = self._root.after(1, self._seek)
