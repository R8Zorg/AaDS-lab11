import enum

class Product:
    def __init__(self, name: str, state: str):
        self.name = name
        self.state = state
        self.with_steam = False



    def cook_time(self) -> int:
        pass

    def __str__(self):
        steam_str = " + пар" if self.with_steam else ""
        return f"{self.name} ({self.state}){steam_str}"

class Meat(Product):
    class ValidStates(enum.Enum):
        FROZEN = "замороженное"
        LOST = "оттаяное"
        READY = "готовое"
        OVERHEATED = "перегретое"

    def __init__(self, state: str):
        if state not in Meat.ValidStates:
            raise ValueError(f"Неверное состояние мяса: {state}"
                             )
        super().__init__("Мясо", state)

    def cook_time(self) -> int:
       times: dict[str,int]  = {
            "замороженное": 300,
            "оттаяное": 180,
            "готовое": 60,
            "перегретое": 30
        }
       print(times["замороженное"])
       base_time = times[self.state]
       if self.with_steam:
           base_time = int(base_time * 0.8)
       return base_time


class Pizza(Product):
    valid_states = {"замороженное", "обычное", "разогретое"}

    def __init__(self, state: str):
        if state not in Pizza.valid_states:
            raise ValueError(f"Неверное состояние пиццы: {state}")
        super().__init__("Пицца", state)

    def cook_time(self) -> int:
        times = {
            "замороженное": 240,
            "обычное": 120,
            "разогретое": 60,
        }
        base_time = times[self.state]
        if self.with_steam:
            base_time = int(base_time * 0.9)
        return base_time


class Popcorn(Product):
    valid_states = {"зерно", "готовое", "сгоревшее"}

    def __init__(self, state: str):
        if state not in Popcorn.valid_states:
            raise ValueError(f"Неверное состояние попкорна: {state}")
        super().__init__("Попкорн", state)

    def cook_time(self) -> int:
        times = {
            "зерно": 180,
            "готовое": 60,
            "сгоревшее": 0,
        }
        base_time = times[self.state]
        if self.with_steam:
            base_time = int(base_time * 0.85)
        return base_time


class Egg(Product):
    def __init__(self, coolness: float):
        """
        coolness: степень остывания, например в градусах или баллах (любое значение)
        """
        super().__init__("Яйцо", "без состояния")
        self.coolness = coolness

    def cook_time(self) -> int:
        # Время готовки яйца — фиксированное, например 90 секунд
        base_time = 90
        if self.with_steam:
            base_time = int(base_time * 0.9)
        return base_time

    def __str__(self):
        steam_str = " + пар" if self.with_steam else ""
        return f"{self.name} (остывание: {self.coolness}){steam_str}"

    def cool_down(self, value: float):
        """
        Метод уменьшения температуры (увеличение степени остывания)
        """
        self.coolness += value
