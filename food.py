from dataclasses import dataclass

import pygame
from pygame import Rect, Surface
from pygame.event import Event

from utils import fetch_resource, load_scaled_image


@dataclass
class FoodState:
    state: str
    cooking_time: int = 0
    may_cool_down: bool = False


@dataclass
class ImageInfo:
    food_state: FoodState
    path: str


class Food:
    INSIDE_OFFSET: int = 20
    MICROWAVE_INSIDE_RECT: Rect

    def __init__(
        self,
        states: list[ImageInfo],
        position: tuple[int, int],
        microwave_inside_rect: Rect,
    ) -> None:
        if states == []:
            raise AttributeError("Список состояний не может быть пустым")

        self.MICROWAVE_INSIDE = microwave_inside_rect
        self.cooked_time: int = 0
        self.cooled_down_time: int = 0
        self.current_food_state: int = 0
        self.max_food_states: int = len(states)
        self.is_inside: bool = False

        self._position: tuple[int, int] = position
        self.size: tuple[int, int] = (350, 250)
        self._states_info: list[ImageInfo] = states
        self._states: dict[str, Surface] = self._convert_states_to_surface()

        self._current_state: Surface = next(iter(self._states.values()))
        self._rect = self._current_state.get_rect(topleft=position)

        self._is_dragging: bool = False
        self._offset_x = 0
        self._offset_y = 0

    def _convert_states_to_surface(self) -> dict[str, Surface]:
        states: dict[str, Surface] = {}
        for info in self._states_info:
            states[info.food_state.state] = load_scaled_image(
                fetch_resource(food=info.path), self.size
            )
        return states

    def heat_up(self, elapsed_time: int) -> None:
        if self.current_food_state >= self.max_food_states - 1:
            return
        self.cooked_time += elapsed_time
        current_state = self._states_info[self.current_food_state]
        if self.cooked_time >= current_state.food_state.cooking_time:
            self.cooked_time = 0
            self.current_food_state += 1
            current_state = self._states_info[self.current_food_state]
            self._current_state = self._states[current_state.food_state.state]

    def cool_down(self, elapsed_time: int) -> None:
        current_state: ImageInfo = self._states_info[self.current_food_state]
        if not current_state.food_state.may_cool_down:
            return

        self.cooled_down_time += elapsed_time
        if self.cooled_down_time >= current_state.food_state.cooking_time:
            print("FF")
            self.cooled_down_time = 0
            self.current_food_state -= 1
            current_state = self._states_info[self.current_food_state]
            self._current_state = self._states[current_state.food_state.state]

    def draw(self, window: Surface) -> None:
        window.blit(self._current_state, self._rect.topleft)

    def _handle_mouse_down(self, event: Event, is_door_closed: bool) -> bool:
        mx, my = event.pos
        if self.is_inside and is_door_closed:
            return False
        if self._rect.collidepoint(mx, my):
            self._is_dragging = True
            self._offset_x = self._rect.x - mx
            self._offset_y = self._rect.y - my
            return True
        return False

    def _handle_mouse_up(self, event: Event, is_door_closed: bool) -> bool:
        self._is_dragging = False
        if self.MICROWAVE_INSIDE.collidepoint(self._rect.center) and not is_door_closed:
            self.is_inside = True
            self._rect.centerx = self.MICROWAVE_INSIDE.centerx
            self._rect.bottom = self.MICROWAVE_INSIDE.bottom - self.INSIDE_OFFSET
            return True
        else:
            self.is_inside = False
            return True

    def _handle_mouse_motion(self, event: Event) -> bool:
        mx, my = event.pos
        if self._is_dragging:
            self._rect.x = mx + self._offset_x
            self._rect.y = my + self._offset_y
            return True
        return False

    def handle_event(self, event: Event, is_door_closed: bool) -> bool:
        if (
            not self._rect.collidepoint(pygame.mouse.get_pos())
            and not self._is_dragging
        ):
            return False
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                return self._handle_mouse_down(event, is_door_closed)
            case pygame.MOUSEBUTTONUP if event:
                return self._handle_mouse_up(event, is_door_closed)
            case pygame.MOUSEMOTION if self._is_dragging:
                return self._handle_mouse_motion(event)
            case _:
                return False
