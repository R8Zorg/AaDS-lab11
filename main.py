import sys

import pygame
from pygame.event import Event

from food_item import FoodItem
from microwave import Microwave
from utils import fetch_resource, load_scaled_image

pygame.init()

WIN_W, WIN_H = 1500, 750
WINDOW = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Микроволновка")


background = load_scaled_image(fetch_resource("background.png"), (WIN_W, WIN_H))


# meat = FoodItem(fetch_resource("meat"), (1100, 260), inside_offset=0)
# pizza = FoodItem(fetch_resource("pizza"), (1100, 370), inside_offset=0)
# popcorn = FoodItem(
#     fetch_resource("popcorn"),
#     (870, 470),
#     inside_offset=0,
#     states_list=["raw", "done", "overheated"],
# )
# egg = FoodItem(
#     fetch_resource("egg"), (1100, 480), inside_offset=0, states_list=["raw", "boom"]
# )

class Button:
    def __init__(self, rect: pygame.Rect, image_off, image_on, callback):
        self.rect = rect
        self.image_off = image_off
        self.image_on = image_on
        self.callback = callback
        self.is_active = False

    def draw(self, surface):
        if self.is_active:
            surface.blit(self.image_on, self.rect.topleft)
        else:
            surface.blit(self.image_off, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_active = not self.is_active
                self.callback(self.is_active)
                return True
        return False
        

if __name__ == "__main__":
    microwave: Microwave = Microwave()
    while microwave.is_running:
        event: Event
        for event in pygame.event.get():
            microwave.on_event(event)

        WINDOW.blit(background, (0, 0))
        WINDOW.blit(microwave.get_body(), microwave.BODY_POSITION)

        microwave.update_door()
        microwave.draw_door(WINDOW)
        # microwave.draw_door_hitboxes(WINDOW)
        microwave.draw_buttons(WINDOW)
        microwave.draw_timer(WINDOW)
        pygame.display.flip()
        pygame.time.Clock().tick(45)

    pygame.quit()
    sys.exit()

# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if not door_locked:
#                 if meat.handle_mouse_down(mx, my):
#                     continue
#                 if pizza.handle_mouse_down(mx, my):
#                     continue
#                 if popcorn.handle_mouse_down(mx, my):
#                     continue
#                 if egg.handle_mouse_down(mx, my):
#                     continue
#
#         if event.type == pygame.MOUSEBUTTONUP:
#             meat.handle_mouse_up()
#             pizza.handle_mouse_up()
#             popcorn.handle_mouse_up()
#             egg.handle_mouse_up()
#
#         if event.type == pygame.MOUSEMOTION:
#             meat.handle_mouse_motion(mx, my)
#             pizza.handle_mouse_motion(mx, my)
#             popcorn.handle_mouse_motion(mx, my)
#             egg.handle_mouse_motion(mx, my)
#
#         if event.type == pygame.KEYDOWN:
#             keys_map = {
#                 pygame.K_1: ("meat", "frozen"),
#                 pygame.K_2: ("meat", "raw"),
#                 pygame.K_3: ("meat", "done"),
#                 pygame.K_4: ("meat", "overheated"),
#                 pygame.K_5: ("pizza", "frozen"),
#                 pygame.K_6: ("pizza", "raw"),
#                 pygame.K_7: ("pizza", "done"),
#                 pygame.K_8: ("pizza", "overheated"),
#                 pygame.K_9: ("popcorn", "raw"),
#                 pygame.K_0: ("popcorn", "done"),
#                 pygame.K_MINUS: ("popcorn", "overheated"),
#                 pygame.K_q: ("egg", "raw"),
#                 pygame.K_w: ("egg", "boom"),
#             }
#
#             if event.key in keys_map:
#                 item, state = keys_map[event.key]
#                 obj = locals()[item]
#                 obj.state = state
#
#                 if item == "egg" and state == "boom":
#                     obj.rect.topleft = BODY_POS
#                     obj.is_boom = True
#
#                 if item == "egg" and state == "raw":
#                     obj.rect = obj.states["raw"].get_rect(topleft=(1100, 480))
#                     obj.is_boom = False
#
#             if event.key == pygame.K_l:
#                 light_on = not light_on
#                 print("Свет:", "включен" if light_on else "выключен")
#
#     if egg.is_boom:
#         WINDOW.blit(egg.states["boom"], BODY_POS)
#     else:
#         WINDOW.blit(body_light if light_on else body, BODY_POS)
#
#     for food in [meat, pizza, popcorn, egg]:
#         if not (food.folder == "egg" and food.is_boom):
#             food.draw(WINDOW, door_index)
