import time

class Microwave:
    def __init__(self):
        self.timer = 0
        self._is_door_opened : bool = False
        self._is_running : bool = False

    def open_door(self):
        self._is_door_opened = True
        self.stop_timer()
        print("Дверца открыта.")

    def close_door(self):
        self._is_door_opened = False
        print("Дверца закрыта.")

    def add_time(self, seconds: int):
        if not self._is_door_opened:
            self.timer += seconds
            print(f"Время увеличено. Текущий таймер: {self.timer} секунд.")

    def reduce_time(self, seconds: int):
        if not self._is_door_opened:
            self.timer = max(0, self.timer - seconds)
            print(f"Время уменьшено. Текущий таймер: {self.timer} секунд.")

    def start(self):
        if self._is_door_opened:
            print("Невозможно запустить: дверь открыта.")
            return
        if self.timer <= 0:
            print("Некорректное время: установите таймер больше нуля.")
            return
        if not self._is_running:
            self._is_running = True
            print("Начинаю работу.")
            self.run_timer()
        else:
            # Если уже работает, добавляем 30 секунд
            self.timer += 30
            print(f"Добавлено 30 секунд. Осталось: {self.timer} секунд.")

    def stop_timer(self):
        if self._is_running:
            self._is_running = False
            print(f"Таймер остановлен. Оставшееся время: {self.timer} секунд.")

    def reset(self):
        self.stop_timer()
        self.timer = 0
        print("Таймер сброшен.")

    def run_timer(self):
        while self._is_running and self.timer > 0:
            print(f"Оставшееся время: {self.timer} секунд.")
            time.sleep(1)
            self.timer -= 1
        if self.timer == 0:
            self._is_running = False
            print("Время закончилось!")


microwave = Microwave()

microwave.open_door()
microwave.close_door()
microwave.add_time(60)
microwave.start()
