import pygame
from pygame import Rect, Surface


class Food:
    """Еда
    Parameters
    ----------
    states: Состояние. Например: {"raw": {"path": "path/to/image.png", "size": 25}}
    position: Позиция середины изображения
    microwave_size: Размер внутренней части микроволновки
    """
    SIZE: tuple[int, int] = pygame.Rect(385, 75, 480, 390)
    MICROWAVE_SIZE: tuple[int, int]
    INSIDE_OFFSET: int = 30

    def __init__(
        self,
        states: dict[str, dict[str, str | int]],
        position: tuple[int, int],
        microwave_size: tuple[int, int],
    ) -> None:
        if states == {}:
            raise AttributeError("Словарь состояний не может быть пустым")
        self.position: tuple[int, int] = position
        self.MICROWAVE_SIZE = microwave_size
        self._states: dict[str, dict[str, str | int]] = states

        self._state_properties: dict[str, str | int] = next(iter(self._states.values()))
        self._current_image: str = next(iter(self._state_properties))
        self.current_state: dict[str, str | int] = next(iter(self._states.values()))
        # self.rect: Rect = 

    def _resize(self, surface: Surface) -> None:
        pass
