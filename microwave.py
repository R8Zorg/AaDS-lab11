import os
import re
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

import pygame
from pygame import Rect, Surface
from pygame.event import Event

from food import Food
from microwave_timer import MicrowaveTimer
from utils import fetch_resource, load_meme_image, load_scaled_image


@dataclass
class Button:
    rect: Rect
    action: Callable[[], None]
    image: str | None = None


class Microwave:
    SIZE = 1500, 750
    BODY_POSITION: tuple[int, int] = (350, 90)
    BODY_SIZE: tuple[int, int] = (700, 450)
    INSIDE_RECT: Rect | None = None
    DOUBLE_CLICK_TIME: int = 30
    CLICK_TIME: int = 10

    def __init__(self) -> None:
        self.width, self.height = self.SIZE
        self.is_door_closed: bool = True
        self._timer = MicrowaveTimer()

        self._last_time: float = 0

        self._body: Surface
        self._body_light: Surface

        self._DOOR_X_POSITION: int = self.BODY_POSITION[0] - 195
        self._DOOR_Y_POSITION: int = self.BODY_POSITION[1] - 65
        self._door_state = 0
        self._is_door_openning: bool = False
        self._is_door_closing: bool = False
        self._door_frames: list[Surface]

        self._DOOR_RECT: Rect = Rect(
            self._DOOR_X_POSITION, self._DOOR_Y_POSITION, 710, 570
        )
        self._closed_door_rect: Rect = Rect(389, 115, 469, 385)
        self._openned_door_rect: Rect = Rect(168, 30, 242, 556)

        self._is_light_on = False
        self._buttons: dict[str, Button]
        self._timer_font: pygame.font.SysFont = pygame.font.SysFont("Arial", 80)

        self._meme_surface: Surface

        self.initialize_data()

    def sort_files_numerically(self, files: list[str]) -> list[str]:
        return sorted(
            files,
            key=lambda name: [
                int(s) if s.isdigit() else s for s in re.split(r"(\d+)", name)
            ],
        )

    def initialize_data(self) -> None:
        frames_folder: str = fetch_resource(microwave="door_frames")
        self._door_frames = [
            load_scaled_image(
                os.path.join(frames_folder, file),
                (self._DOOR_RECT.w, self._DOOR_RECT.h),
            )
            for file in self.sort_files_numerically(os.listdir(frames_folder))
            if file.endswith(".png")
        ]

        buttons_folder = fetch_resource(microwave="buttons")
        self._meme_surface = load_meme_image(fetch_resource(meme="1.jpg"), (170, 170))
        self._buttons = {
            "timer": Button(Rect(875, 125, 155, 65), self.on_timer_click),
            "double_left": Button(Rect(870, 397, 30, 40), self.on_double_left_click),
            "left": Button(Rect(910, 396, 25, 41), self.on_left_click),
            "right": Button(Rect(970, 397, 25, 40), self.on_right_click),
            "double_right": Button(Rect(1005, 397, 30, 40), self.on_double_right_click),
            "start": Button(Rect(955, 445, 85, 60), self.on_start_click),
            "stop": Button(Rect(865, 445, 85, 60), self.on_stop_click),
        }

        for name, button in self._buttons.items():
            path: str = os.path.join(buttons_folder, f"{name}.png")
            if os.path.exists(path):
                button.image = load_scaled_image(path, button.rect.size)

        self._body = load_scaled_image(
            fetch_resource(microwave="microwave.png"), self.BODY_SIZE
        )
        self._body_light = load_scaled_image(
            fetch_resource(microwave="microwave_light.png"), self.BODY_SIZE
        )
        self.INSIDE_RECT = self._closed_door_rect

    def set_food_list(self, food_list: list[Food]) -> None:
        self._food_list = food_list

    def get_body(self) -> Surface:
        return self._body_light if self._is_light_on else self._body

    def on_timer_click(self) -> None:
        print("Нажата кнопка: timer")

    def on_double_left_click(self) -> None:
        self._timer.add_seconds(-self.DOUBLE_CLICK_TIME)

    def on_left_click(self) -> None:
        self._timer.add_seconds(-self.CLICK_TIME)

    def on_right_click(self) -> None:
        self._timer.add_seconds(self.CLICK_TIME)

    def on_double_right_click(self) -> None:
        self._timer.add_seconds(self.DOUBLE_CLICK_TIME)

    def on_start_click(self) -> None:
        if self.is_door_closed:
            self._last_time = time.time()
            self._timer.start()

    def on_stop_click(self) -> None:
        if self._timer.is_on_pause:
            self._timer.reset()
        else:
            self._timer.pause()

    def draw_meme(self, surface: Surface) -> None:
        surface.blit(self._meme_surface, (867, 207))

    def draw_timer(self, surface: Surface) -> None:
        if self._timer.is_showing_time:
            current_time: str = datetime.now().strftime("%H:%M")
        else:
            self._timer.update()
            current_time = self._timer.get_time_str()
        color: tuple[int, int, int] = (255, 255, 255)
        time_surface = self._timer_font.render(current_time, True, color)
        text_rect: Rect = time_surface.get_rect(
            center=self._buttons["timer"].rect.center
        )
        surface.blit(time_surface, text_rect)

    def draw_buttons(self, surface: Surface) -> None:
        for _, button in self._buttons.items():
            surface.blit(button.image, button.rect.topleft)

    def draw_door_hitboxes(self, surface: Surface) -> None:
        pygame.draw.rect(surface, (0, 255, 0), self._closed_door_rect, 2)
        pygame.draw.rect(surface, (0, 255, 0), self._openned_door_rect, 2)

    def draw_door(self, surface: Surface) -> None:
        door: Surface = self._door_frames[self._door_state]
        surface.blit(door, self._DOOR_RECT.topleft)

    def update_food(self) -> None:
        now: float = time.time()
        time_elapsed: int = int(now - self._last_time)
        if time_elapsed < 1:
            return
        for food in self._food_list:
            if self.is_door_closed and self._timer.is_running and food.is_inside:
                food.heat_up(time_elapsed)
            else:
                food.cool_down(time_elapsed)
        self._last_time = now

    def update_door(self) -> None:
        if self._is_door_openning:
            if self._door_state < len(self._door_frames) - 1:
                self._door_state += 1
            else:
                self._is_door_openning = False
                self._timer.pause()
                self._last_time = time.time()
        elif self._is_door_closing:
            if self._door_state > 0:
                self._door_state -= 1
            else:
                self._is_door_closing = False
                self.is_door_closed = True

    def handle_event(self, event: Event) -> None:
        mx, my = pygame.mouse.get_pos()
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                for _, button in self._buttons.items():
                    if button.rect.collidepoint(mx, my):
                        button.action()
                if bool(self._is_door_openning + self._is_door_closing) is True:
                    return
                if self._closed_door_rect.collidepoint(mx, my):
                    self.is_door_closed = False
                    self._is_door_openning = True
                    return
                if self._openned_door_rect.collidepoint(mx, my):
                    self._is_door_closing = True
                    return
