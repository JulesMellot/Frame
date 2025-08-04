"""Simple scheduler for periodic tasks."""
from __future__ import annotations

import threading
from typing import Callable


class Scheduler:
    """Run ``func`` every ``interval`` seconds in a background thread."""

    def __init__(self, interval: int, func: Callable[[], None]):
        self.interval = interval
        self.func = func
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def _run(self) -> None:
        while not self._stop_event.wait(self.interval):
            self.func()

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        self._thread.join()
