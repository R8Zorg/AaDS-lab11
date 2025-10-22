from dataclasses import dataclass

import pygame
from pygame import Surface
from pygame.event import Event

from utils import fetch_resource, load_scaled_image


@dataclass
class ImageInfo:
    state: str
    path: str


class Food:
    INSIDE_OFFSET: int = 30

    def __init__(
        self,
        states: list[ImageInfo],
        size: tuple[int, int],
        position: tuple[int, int],
    ) -> None:
        if states == []:
            raise AttributeError("Список состояний не может быть пустым")

        self._position: tuple[int, int] = position
        self._size: tuple[int, int] = size
        self._states_info: list[ImageInfo] = states
        self._states: dict[str, Surface] = {}
        self._current_state: Surface = None

        self._convert_states_to_surface()

        self._is_dragging: bool = False
        self._drag_offset: tuple[int, int] = (0, 0)

    def _convert_states_to_surface(self) -> None:
        info: ImageInfo
        for info in self._states_info:
            self._states[info.state] = load_scaled_image(
                fetch_resource(food=info.path), self._size
            )
        self._current_state = next(iter(self._states.values()))

    def draw(self, window: Surface) -> None:
        if self._current_state:
            window.blit(self._current_state, self._position)

    def _on_mouse_down(self, event: Event) -> None:
        rect = self._current_state.get_rect(topleft=self._position)
        if rect.collidepoint(pygame.mouse.get_pos()):
            self._is_dragging = True
            self._drag_offset = (
                self._position[0] - event.pos[0],
                self._position[1] - event.pos[1],
            )

    def on_event(self, event: Event) -> None:
        mx, my = pygame.mouse.get_pos()
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                self._on_mouse_down(event)
            case pygame.MOUSEBUTTONUP if event:
                self._is_dragging = False
            case pygame.MOUSEMOTION if self._is_dragging:
                self._position = (mx + self._drag_offset[0], my + self._drag_offset[1])
