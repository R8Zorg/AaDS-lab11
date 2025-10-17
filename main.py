import os
import re
import pygame

pygame.init()

WIN_W, WIN_H = 1500, 750
WIN = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Микроволновка")

clock = pygame.time.Clock()

def sort_files_numerically(files):
    return sorted(files, key=lambda name: [int(s) if s.isdigit() else s for s in re.split(r"(\d+)", name)])

def load_scaled_image(path, size):
    return pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)

background = load_scaled_image("fon.png", (WIN_W, WIN_H))
BODY_SIZE = (int(800 * 0.875), int(600 * 0.75))
BODY_POS = (350, 90)
body = load_scaled_image("1.png", BODY_SIZE)
body_light = load_scaled_image("1_light.png", BODY_SIZE)
light_on = False

WINDOW_RECT = pygame.Rect(BODY_POS[0] - 195, BODY_POS[1] - 65, 710, 570)
frames_folder = "frames2"
door_frames = [load_scaled_image(os.path.join(frames_folder, f), (WINDOW_RECT.w, WINDOW_RECT.h))
               for f in sort_files_numerically(os.listdir(frames_folder)) if f.endswith(".png")]
door_index = 0
door_opening = door_closing = door_locked = False

FOOD_HITBOX = pygame.Rect(385, 75, 480, 390)

class FoodItem:
    def __init__(self, folder, pos, inside_offset=30, states_list=None):
        if states_list is None:
            states_list = ["frozen", "raw", "done", "overheated"]
        self.folder = folder
        self.states = {}
        for state in states_list:
            if state == "boom":
                self.states[state] = load_scaled_image(os.path.join(folder, f"{state}.png"), BODY_SIZE)
            else:
                self.states[state] = load_scaled_image(os.path.join(folder, f"{state}.png"), (350, 250))
        self.state = states_list[0]
        self.rect = self.states[self.state].get_rect(topleft=pos)
        self.dragging = self.inside = self.locked = False
        self.offset_x = self.offset_y = 0
        self.inside_offset = inside_offset
        self.is_boom = False

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
                if self.folder == "egg":
                    self.is_boom = False
            else:
                self.inside = False
                if self.folder == "egg" and self.state == "boom":
                    fallback_state = "raw" if "raw" in self.states else list(self.states.keys())[0]
                    self.state = fallback_state
                    self.rect = self.states[self.state].get_rect(topleft=(1100, 480))
                    self.is_boom = False

    def handle_mouse_motion(self, mx, my):
        if self.dragging and not self.locked:
            self.rect.x = mx + self.offset_x
            self.rect.y = my + self.offset_y

    def draw(self, surface, door_index):
        surface.blit(self.states[self.state], self.rect.topleft)

meat = FoodItem("meat", (1100, 260), inside_offset=0)
pizza = FoodItem("pizza", (1100, 370), inside_offset=0)
popcorn = FoodItem("popcorn", (870, 470), inside_offset=0, states_list=["raw", "done", "overheated"])
egg = FoodItem("egg", (1100, 480), inside_offset=0, states_list=["raw", "boom"])

buttons_folder = "buttons"
button_data = [
    ("timer", (875, 125), (155, 65)),
    ("frozen", (875, 207), (150, 60)),
    ("double_left", (868, 282), (30, 38)),
    ("left", (901, 280), (25, 40)),
    ("ok", (930, 280), (40, 40)),
    ("right", (975, 280), (25, 40)),
    ("double_right", (1005, 280), (30, 40)),
    ("start", (897, 340), (100, 60)),
    ("stop", (897, 420), (100, 60)),
]
buttons = [{"name": name, "image": load_scaled_image(os.path.join(buttons_folder, f"{name}.png"), size),
            "rect": pygame.Rect(pos, size)}
           for name, pos, size in button_data if os.path.exists(os.path.join(buttons_folder, f"{name}.png"))]

timer_font = pygame.font.SysFont("Arial", 50)
timer_text = "00:00"

# --- Методы для кнопок ---
def timer_button():
    print("Нажата кнопка: timer")

def frozen_button():
    print("Нажата кнопка: frozen")

def double_left_button():
    print("Нажата кнопка: double_left")

def left_button():
    print("Нажата кнопка: left")

def ok_button():
    print("Нажата кнопка: ok")

def right_button():
    print("Нажата кнопка: right")

def double_right_button():
    print("Нажата кнопка: double_right")

def start_button():
    print("Нажата кнопка: start")

def stop_button():
    print("Нажата кнопка: stop")

running = True
while running:
    mx = my = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION]:
            mx, my = event.pos

        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in buttons:
                if btn["rect"].collidepoint(mx, my):
                    func_name = f"{btn['name']}_button"
                    if func_name in globals():
                        globals()[func_name]()
                    else:
                        print(f"Нажата кнопка: {btn['name']}")
                    break

            if not door_locked:
                if meat.handle_mouse_down(mx, my): continue
                if pizza.handle_mouse_down(mx, my): continue
                if popcorn.handle_mouse_down(mx, my): continue
                if egg.handle_mouse_down(mx, my): continue

                if WINDOW_RECT.collidepoint(mx, my):
                    if door_index == 0:
                        door_opening, door_closing = True, False
                        door_locked = True
                        meat.locked = pizza.locked = popcorn.locked = egg.locked = False
                    elif door_index == len(door_frames)-1:
                        door_closing, door_opening = True, False
                        door_locked = True
                    continue

        if event.type == pygame.MOUSEBUTTONUP:
            meat.handle_mouse_up()
            pizza.handle_mouse_up()
            popcorn.handle_mouse_up()
            egg.handle_mouse_up()

        if event.type == pygame.MOUSEMOTION:
            meat.handle_mouse_motion(mx, my)
            pizza.handle_mouse_motion(mx, my)
            popcorn.handle_mouse_motion(mx, my)
            egg.handle_mouse_motion(mx, my)

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
                pygame.K_9: ("popcorn", "raw"),
                pygame.K_0: ("popcorn", "done"),
                pygame.K_MINUS: ("popcorn", "overheated"),

                pygame.K_q: ("egg", "raw"),
                pygame.K_w: ("egg", "boom"),
            }

            if event.key in keys_map:
                item, state = keys_map[event.key]
                obj = locals()[item]
                obj.state = state

                if item == "egg" and state == "boom":
                    obj.rect.topleft = BODY_POS
                    obj.is_boom = True

                if item == "egg" and state == "raw":
                    obj.rect = obj.states["raw"].get_rect(topleft=(1100, 480))
                    obj.is_boom = False

            if event.key == pygame.K_l:
                light_on = not light_on
                print("Свет:", "включен" if light_on else "выключен")

    if door_opening:
        door_index = min(door_index+1, len(door_frames)-1)
        if door_index == len(door_frames)-1:
            door_opening = False
            door_locked = meat.locked = pizza.locked = popcorn.locked = egg.locked = False
    elif door_closing:
        door_index = max(door_index-1, 0)
        if door_index == 0:
            door_closing = False
            door_locked = False
            meat.locked = meat.inside
            pizza.locked = pizza.inside
            popcorn.locked = popcorn.inside
            egg.locked = egg.inside

    WIN.blit(background, (0, 0))

    if egg.is_boom:
        WIN.blit(egg.states["boom"], BODY_POS)
    else:
        if light_on:
            WIN.blit(body_light, BODY_POS)
        else:
            WIN.blit(body, BODY_POS)

    for item in [meat, pizza, popcorn, egg]:
        if not (item.folder == "egg" and item.is_boom):
            item.draw(WIN, door_index)

    WIN.blit(door_frames[door_index], WINDOW_RECT.topleft)

    for btn in buttons:
        WIN.blit(btn["image"], btn["rect"].topleft)
    WIN.blit(timer_font.render(timer_text, True, (255, 0, 0)), (890, 130))

    pygame.display.flip()
    clock.tick(45)

pygame.quit()
