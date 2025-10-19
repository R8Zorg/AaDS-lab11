import os
import re

import pygame
from pygame import Rect, Surface
from pygame.event import Event

from utils import fetch_resource, load_scaled_image


class Microwave:
    def __init__(self) -> None:
        self.is_running: bool = False
        self.SIZE = self.width, self.height = 1500, 750
        self.BODY_POSITION: tuple[int, int] = (350, 90)

        self._BODY_SIZE: tuple[int, int] = (int(800 * 0.875), int(600 * 0.75))
        self._body: Surface
        self._body_light: Surface

        self._DOOR_X_POSITION: int = self.BODY_POSITION[0] - 195
        self._DOOR_Y_POSITION: int = self.BODY_POSITION[1] - 65
        self._DOOR_RECT: Rect = Rect(
            self._DOOR_X_POSITION, self._DOOR_Y_POSITION, 710, 570
        )
        self._closed_door_rect: Rect = Rect(390, 115, 470, 385)
        self._openned_door_rect: Rect = Rect(169, 30, 242, 556)
        self._door_state = 0
        self._is_door_closed: bool = True
        self._is_door_openning: bool = False
        self._is_door_closing: bool = False
        self._door_frames: list[Surface]

        self._is_light_on = False
        self._button_data: list[tuple[str, tuple[int, int], tuple[int, int], object]]
        self._buttons: list[dict[str, str | Surface | Rect]]
        self._timer_font: pygame.font.SysFont = pygame.font.SysFont("Arial", 74)
        self._timer_text: any = "00:00"  # WARN: type: any

        self.initialize_data()

    def sort_files_numerically(self, files: list[str]) -> list[str]:
        return sorted(
            files,
            key=lambda name: [
                int(s) if s.isdigit() else s for s in re.split(r"(\d+)", name)
            ],
        )

    def initialize_data(self) -> None:
        frames_folder: str = fetch_resource("door_frames")
        self._door_frames = [
            load_scaled_image(
                os.path.join(frames_folder, file),
                (self._DOOR_RECT.w, self._DOOR_RECT.h),
            )
            for file in self.sort_files_numerically(os.listdir(frames_folder))
            if file.endswith(".png")
        ]

        buttons_folder = fetch_resource("buttons")
        self._button_data = [
            ("timer", (875, 125), (155, 65), self.on_timer_click),
            ("frozen", (875, 207), (150, 60), self.on_quick_defrost_click),
            ("double_left", (868, 282), (30, 38), self.on_double_left_click),
            ("left", (901, 280), (25, 40), self.on_left_click),
            ("ok", (930, 280), (40, 40), self.on_ok_click),
            ("right", (975, 280), (25, 40), self.on_right_click),
            ("double_right", (1005, 280), (30, 40), self.on_double_right_click),
            ("start", (897, 340), (100, 60), self.on_start_click),
            ("stop", (897, 420), (100, 60), self.on_stop_click),
        ]

        self._buttons = [
            {
                "name": name,
                "image": load_scaled_image(
                    os.path.join(buttons_folder, f"{name}.png"), size
                ),
                "rect": Rect(pos, size),
                "action": action,
            }
            for name, pos, size, action in self._button_data
            if os.path.exists(os.path.join(buttons_folder, f"{name}.png"))
        ]

        self._body = load_scaled_image(fetch_resource("microwave.png"), self._BODY_SIZE)
        self._body_light = load_scaled_image(
            fetch_resource("microwave_light.png"), self._BODY_SIZE
        )

        self.is_running = True

    def get_body(self) -> Surface:
        return self._body_light if self._is_light_on else self._body

    def on_timer_click(self) -> None:
        print("Нажата кнопка: timer")

    def on_quick_defrost_click(self) -> None:
        print("Нажата кнопка: frozen")

    def on_double_left_click(self) -> None:
        print("Нажата кнопка: double_left")

    def on_left_click(self) -> None:
        print("Нажата кнопка: left")

    def on_ok_click(self) -> None:
        print("Нажата кнопка: ok")

    def on_right_click(self) -> None:
        print("Нажата кнопка: right")

    def on_double_right_click(self) -> None:
        print("Нажата кнопка: double_right")

    def on_start_click(self) -> None:
        print("Нажата кнопка: start")

    def on_stop_click(self) -> None:
        print("Нажата кнопка: stop")

    def draw_timer(self, surface: Surface) -> None:
        surface.blit(
            self._timer_font.render(self._timer_text, True, (0, 255, 0)), (880, 130)
        )

    def draw_buttons(self, surface: Surface) -> None:
        for button in self._buttons:
            surface.blit(button["image"], button["rect"].topleft)

    def draw_door_hitboxes(self, surface: Surface) -> None:
        pygame.draw.rect(surface, (0, 255, 0), self._closed_door_rect, 2)
        pygame.draw.rect(surface, (0, 255, 0), self._openned_door_rect, 2)

    def draw_door(self, surface: Surface) -> None:
        door: Surface = self._door_frames[self._door_state]
        surface.blit(door, self._DOOR_RECT.topleft)

    def update_door(self) -> None:
        if self._is_door_openning:
            if self._door_state < len(self._door_frames) - 1:
                self._door_state += 1
            else:
                self._is_door_openning = False
        elif self._is_door_closing:
            if self._door_state > 0:
                self._door_state -= 1
            else:
                self._is_door_closing = False
                self._is_door_closed = True

    def on_event(self, event: Event) -> None:
        mx, my = pygame.mouse.get_pos()
        match event.type:
            case pygame.QUIT:
                self.is_running = False
            case pygame.MOUSEBUTTONDOWN:
                for button in self._buttons:
                    if button["rect"].collidepoint(mx, my):  # type: ignore
                        button["action"]()  # type: ignore
                if bool(self._is_door_openning + self._is_door_closing) is True:
                    return
                if self._closed_door_rect.collidepoint(mx, my):
                    self._is_door_closed = False
                    self._is_door_openning = True
                    return
                if self._openned_door_rect.collidepoint(mx, my):
                    self._is_door_closing = True
                    return
