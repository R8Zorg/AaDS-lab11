import time
from datetime import datetime, timedelta


class MicrowaveTimer:
    def __init__(self) -> None:
        self.is_showing_time: bool = True
        self._seconds: int = 0
        self.is_on_pause: bool = False
        self._last_time: float | None = None
        self._blink_state: bool = True
        self._blink_timer: float = 0.0
        self._blink_interval: float = 0.5
        self._blink_count: int = 0
        self._max_blinks: int = 6

    def add_seconds(self, seconds: int) -> None:
        self._seconds = max(0, self._seconds + seconds)
        if self._seconds != 0:
            self.is_showing_time = False

    def start(self) -> None:
        if self._seconds > 0:
            self.is_showing_time = False
            self.is_on_pause = False
            self._last_time = time.time()

    def pause(self) -> None:
        if not self.is_showing_time:
            self.is_on_pause = True
            self._last_time = None

    def reset(self) -> None:
        self.is_showing_time = True
        self.is_on_pause = False
        self._seconds = 0
        self._last_time = None
        self._blink_count = 0

    def update(self) -> None:
        if self.is_showing_time:
            return

        if self._seconds == 0 and not self.is_on_pause:
            if self._blink_count < self._max_blinks:
                now = time.time()
                if now - self._blink_timer > self._blink_interval:
                    self._blink_state = not self._blink_state
                    self._blink_timer = now
                    self._blink_count += 1
            else:
                self.reset()
            return

        if not self.is_on_pause and self._last_time is not None:
            now = time.time()
            elapsed = now - self._last_time
            if elapsed >= 1:
                self._seconds = max(0, self._seconds - int(elapsed))
                self._last_time = now
                if self._seconds == 0:
                    self._blink_timer = time.time()
                    self._blink_state = True
                    self._blink_count = 0

    def get_time_str(self) -> str:
        if self.is_showing_time:
            now = datetime.now().strftime("%H:%M")
            return now

        if self._seconds == 0 and not self.is_on_pause:
            return "" if not self._blink_state else "00:00"

        time_delta = timedelta(seconds=self._seconds)
        minutes, seconds = divmod(time_delta.seconds, 60)
        return f"{minutes:02}:{seconds:02}"
