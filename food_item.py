import os

import pygame

from utils import load_scaled_image

BODY_SIZE = (int(800 * 0.875), int(600 * 0.75))
FOOD_HITBOX = pygame.Rect(385, 75, 480, 390)


class FoodItem:
    def __init__(
        self,
        folder: str,
        pos: tuple[int, int],
        inside_offset: int = 30,  # WARN: ??
        states_list: list[str] = None,
    ) -> None:
        if states_list is None:
            states_list = ["frozen", "raw", "done", "overheated"]
        self.folder = folder
        self.states = {}
        for state in states_list:
            if state == "boom":
                self.states[state] = load_scaled_image(
                    os.path.join(folder, f"{state}.png"),
                    BODY_SIZE,  # TODO: microvave.BODY_SIZE
                )
            else:
                self.states[state] = load_scaled_image(
                    os.path.join(folder, f"{state}.png"), (350, 250)
                )
        self.state = states_list[0]
        self.rect = self.states[self.state].get_rect(topleft=pos)
        self.is_dragging = self.is_inside = self.is_locked = False
        self.offset_x = self.offset_y = 0
        self.inside_offset = inside_offset
        self.is_boom = False
        self._object_name = folder.split("/")[1]

    def handle_mouse_down(self, mx: int, my: int) -> bool:  # WARN: rename
        if not self.is_locked and self.rect.collidepoint(mx, my):
            self.is_dragging = True
            self.offset_x = self.rect.x - mx
            self.offset_y = self.rect.y - my
            return True
        return False

    def handle_mouse_up(self):
        if not self.is_dragging:
            return
        self.is_dragging = False
        if FOOD_HITBOX.collidepoint(self.rect.center):
            self.is_inside = True
            self.rect.centerx = FOOD_HITBOX.centerx
            self.rect.bottom = FOOD_HITBOX.bottom - self.inside_offset
            if self._object_name == "egg":  # WARN: ??
                self.is_boom = False
        else:
            self.is_inside = False
            # WARN: folder = "resources/name", not "name"
            if self._object_name == "egg" and self.state == "boom":  # WARN: !!
                fallback_state = (
                    "raw" if "raw" in self.states else list(self.states.keys())[0]
                )
                self.state = fallback_state
                self.rect = self.states[self.state].get_rect(
                    topleft=(1100, 480)
                )  # WARN: hardcoded coordinates
                self.is_boom = False

    def handle_mouse_motion(self, mx: int, my: int) -> None:
        if self.is_dragging and not self.is_locked:
            self.rect.x = mx + self.offset_x
            self.rect.y = my + self.offset_y

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.states[self.state], self.rect.topleft)
