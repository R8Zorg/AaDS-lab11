import time
from datetime import datetime, timedelta


class MicrowaveTimer:
    def __init__(self) -> None:
        self.is_showing_time: bool = True
        self.is_running: bool = False
        self.seconds: int = 0
        self.elapsed_seconds: int = 0
        self.is_on_pause: bool = False
        self._previous_time: float | None = None

        self._blink_state: bool = True
        self._blink_last_time: float = 0.0
        self._blink_interval: float = 0.5
        self._blink_count: int = 0
        self._max_blinks: int = 5

    def add_seconds(self, seconds: int) -> None:
        self.seconds = max(0, self.seconds + seconds)
        if self.seconds != 0:
            self.is_showing_time = False
        else:
            self.reset()

    def start(self) -> None:
        if self.seconds > 0:
            self.is_showing_time = False
            self.is_running = True
            self.is_on_pause = False
            self._previous_time = time.time()

    def pause(self) -> None:
        if not self.is_showing_time:
            self.is_on_pause = True
            self.is_running = False
            self._previous_time = None

    def reset(self) -> None:
        self.is_showing_time = True
        self.is_running = False
        self.is_on_pause = False
        self.seconds = 0
        self._previous_time = None
        self._blink_count = 0
        self.elapsed_seconds = 0

    def update(self) -> None:
        if self.is_showing_time:
            return

        if self.seconds == 0 and not self.is_on_pause:
            now = time.time()
            if now - self._blink_last_time > self._blink_interval:
                if self._blink_count < self._max_blinks:
                    self._blink_state = not self._blink_state
                    self._blink_last_time = time.time()
                    self._blink_count += 1
                else:
                    self.reset()
            return

        if not self.is_on_pause and self._previous_time is not None:
            now = time.time()
            elapsed = now - self._previous_time
            if elapsed >= 1:
                self.seconds = max(0, self.seconds - int(elapsed))
                self.elapsed_seconds += int(elapsed)
                self._previous_time = now
                if self.seconds == 0:
                    self._previous_time = None
                    self._blink_last_time = time.time()
                    self._blink_state = True
                    self._blink_count = 0

    def get_time_str(self) -> str:
        if self.is_showing_time:
            return datetime.now().strftime("%H:%M")

        if self.seconds == 0 and not self.is_on_pause:
            return "" if not self._blink_state else "00:00"

        time_delta = timedelta(seconds=self.seconds)
        minutes, seconds = divmod(time_delta.seconds, 60)
        return f"{minutes:02}:{seconds:02}"
