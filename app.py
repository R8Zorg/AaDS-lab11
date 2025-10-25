import sys

import pygame
from pygame import Surface

from food import Food
from microwave import Microwave
from utils import fetch_resource, load_scaled_image


class App:
    FPS: int = 60

    def __init__(
        self,
        main_window: Surface,
        background_image: str,
        microwave: Microwave,
        food_list: list[Food],
    ) -> None:
        self._main_window: Surface = main_window
        self._microwave: Microwave = microwave
        self._food_list: list[Food] = food_list
        self._is_initialized: bool = False
        self._background: Surface = load_scaled_image(
            fetch_resource(background_image), main_window.get_size()
        )

    def _draw_food(self) -> None:
        reversed_food_list: list[Food] = self._food_list.copy()
        reversed_food_list.reverse()
        for food in reversed_food_list:
            food.draw(self._main_window)

    def _is_food_inside(self) -> bool:
        for food in self._food_list:
            if food.is_inside:
                return True
        return False

    def _render(self) -> None:
        self._main_window.blit(self._background, (0, 0))
        self._main_window.blit(
            self._microwave.get_body(), self._microwave.BODY_POSITION
        )

        self._microwave.draw_buttons(self._main_window)
        self._microwave.draw_timer(self._main_window)
        self._microwave.update_door()

        if self._is_food_inside():
            self._draw_food()
            self._microwave.draw_door(self._main_window)
        else:
            self._microwave.draw_door(self._main_window)
            self._draw_food()

        pygame.display.flip()

    def run(self) -> None:
        clock: pygame.time.Clock = pygame.time.Clock()

        dragged_food: Food | None = None
        is_running = True
        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                    break

                if dragged_food:
                    dragged_food.handle_event(event, self._microwave.is_door_closed)
                    if event.type == pygame.MOUSEBUTTONUP:
                        dragged_food = None
                    continue

                for food in self._food_list:
                    if food.handle_event(event, self._microwave.is_door_closed):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            dragged_food = food
                        break
                else:
                    self._microwave.handle_event(event)
            self._render()
            clock.tick(self.FPS)

        pygame.quit()
        sys.exit()
