import os
import re
import pygame

pygame.init()

WIN_W, WIN_H = 1500, 650
WIN = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Микроволновка")

clock = pygame.time.Clock()

def sort_files_numerically(files):
    return sorted(files, key=lambda name: [int(s) if s.isdigit() else s for s in re.split(r"(\d+)", name)])

def load_scaled_image(path, size):
    return pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)

background = load_scaled_image("fon.png", (WIN_W, WIN_H))
BODY_SIZE = (int(800 * 0.875), int(600 * 0.75))
BODY_POS = (350, 50)
body = load_scaled_image("1.png", BODY_SIZE)

WINDOW_RECT = pygame.Rect(BODY_POS[0] - 195, BODY_POS[1] - 65, 710, 570)
frames_folder = "frames2"
door_frames = [load_scaled_image(os.path.join(frames_folder, f), (WINDOW_RECT.w, WINDOW_RECT.h))
               for f in sort_files_numerically(os.listdir(frames_folder)) if f.endswith(".png")]
door_index = 0
door_opening = door_closing = door_locked = False

FOOD_HITBOX = pygame.Rect(385, 75, 480, 390)

class FoodItem:
    def __init__(self, folder, pos, inside_offset=30):
        self.states = {state: load_scaled_image(os.path.join(folder, f"{state}.png"), (350, 250))
                       for state in ["raw", "frozen", "done", "overheated"]}
        self.state = "frozen"
        self.rect = self.states[self.state].get_rect(topleft=pos)
        self.dragging = self.inside = self.locked = False
        self.offset_x = self.offset_y = 0
        self.inside_offset = inside_offset

    def handle_mouse_down(self, mx, my):
        if not self.locked and self.rect.collidepoint(mx, my):
            self.dragging = True
            self.offset_x = self.rect.x - mx
            self.offset_y = self.rect.y - my
            return True
        return False

    def handle_mouse_up(self):
        if self.dragging:
            self.dragging = False
            if FOOD_HITBOX.collidepoint(self.rect.center):
                self.inside = True
                self.rect.centerx = FOOD_HITBOX.centerx
                self.rect.bottom = FOOD_HITBOX.bottom - self.inside_offset
            else:
                self.inside = False

    def handle_mouse_motion(self, mx, my):
        if self.dragging and not self.locked:
            self.rect.x = mx + self.offset_x
            self.rect.y = my + self.offset_y

    def draw(self, surface, door_index):
        if self.inside:
            surface.blit(self.states[self.state], self.rect.topleft)
        if not self.inside or door_index == 0:
            surface.blit(self.states[self.state], self.rect.topleft)

meat = FoodItem("meat", (1100, 240), inside_offset=30)
pizza = FoodItem("pizza", (1100, 350), inside_offset=30)

buttons_folder = "buttons"
button_data = [
    ("timer", (875, 85), (155, 65)),
    ("frozen", (875, 167), (150, 60)),
    ("double_left", (868, 242), (30, 38)),
    ("left", (901, 240), (25, 40)),
    ("ok", (930, 240), (40, 40)),
    ("right", (975, 240), (25, 40)),
    ("double_right", (1005, 240), (30, 40)),
    ("start", (897, 300), (100, 60)),
    ("stop", (897, 380), (100, 60)),
]

buttons = [{"name": name, "image": load_scaled_image(os.path.join(buttons_folder, f"{name}.png"), size),
            "rect": pygame.Rect(pos, size)}
           for name, pos, size in button_data if os.path.exists(os.path.join(buttons_folder, f"{name}.png"))]

def on_timer(): print("Событие кнопки: timer")
def on_frozen(): print("Событие кнопки: frozen")
def on_double_left(): print("Событие кнопки: double_left")
def on_left(): print("Событие кнопки: left")
def on_ok(): print("Событие кнопки: ok")
def on_right(): print("Событие кнопки: right")
def on_double_right(): print("Событие кнопки: double_right")
def on_start(): print("Событие кнопки: start")
def on_stop(): print("Событие кнопки: stop")

button_actions = {
    "timer": on_timer,
    "frozen": on_frozen,
    "double_left": on_double_left,
    "left": on_left,
    "ok": on_ok,
    "right": on_right,
    "double_right": on_double_right,
    "start": on_start,
    "stop": on_stop,
}

timer_font = pygame.font.SysFont("Arial", 40)
timer_text = "00:00"

running = True
while running:
    mx = my = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION]:
            mx, my = event.pos

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not door_locked:
                if meat.handle_mouse_down(mx, my): continue
                if pizza.handle_mouse_down(mx, my): continue

                if WINDOW_RECT.collidepoint(mx, my):
                    if door_index == 0:
                        door_opening, door_closing = True, False
                        door_locked = True
                        meat.locked = pizza.locked = False
                    elif door_index == len(door_frames)-1:
                        door_closing, door_opening = True, False
                        door_locked = True
                    continue

                if door_index == 0:
                    for btn in buttons:
                        if btn["rect"].collidepoint(mx, my):
                            button_actions[btn["name"]]()  # фронт-событие
                            break

        if event.type == pygame.MOUSEBUTTONUP:
            meat.handle_mouse_up()
            pizza.handle_mouse_up()

        if event.type == pygame.MOUSEMOTION:
            meat.handle_mouse_motion(mx, my)
            pizza.handle_mouse_motion(mx, my)

        if event.type == pygame.KEYDOWN:
            keys_map = {
                pygame.K_1: ("meat", "frozen"),
                pygame.K_2: ("meat", "raw"),
                pygame.K_3: ("meat", "done"),
                pygame.K_4: ("meat", "overheated"),
                pygame.K_5: ("pizza", "frozen"),
                pygame.K_6: ("pizza", "raw"),
                pygame.K_7: ("pizza", "done"),
                pygame.K_8: ("pizza", "overheated"),
            }
            if event.key in keys_map:
                item, state = keys_map[event.key]
                locals()[item].state = state

    # --- Анимация дверцы ---
    if door_opening:
        door_index = min(door_index+1, len(door_frames)-1)
        if door_index == len(door_frames)-1:
            door_opening = False
            door_locked = meat.locked = pizza.locked = False
    elif door_closing:
        door_index = max(door_index-1, 0)
        if door_index == 0:
            door_closing = False
            door_locked = False
            meat.locked = meat.inside
            pizza.locked = pizza.inside

    WIN.blit(background, (0, 0))
    WIN.blit(body, BODY_POS)
    for btn in buttons:
        WIN.blit(btn["image"], btn["rect"].topleft)

    meat.draw(WIN, door_index)
    pizza.draw(WIN, door_index)
    WIN.blit(door_frames[door_index], WINDOW_RECT.topleft)
    WIN.blit(timer_font.render(timer_text, True, (255, 0, 0)), (880, 100))

    pygame.display.flip()
    clock.tick(45)

pygame.quit()