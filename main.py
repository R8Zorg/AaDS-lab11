import os
import re

import pygame

pygame.init()

# === Константы ===
WIN_W, WIN_H = 1200, 600
FPS = 45

WIN = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Микроволновка")


# === Утилиты ===
def sort_files_numerically(files: list[str]) -> list[str]:
    """Сортирует список файлов по числам в названии."""
    return sorted(
        files,
        key=lambda name: [
            int(s) if s.isdigit() else s for s in re.split(r"(\d+)", name)
        ],
    )


def load_scaled_image(path: str, size: tuple[int, int]) -> pygame.Surface:
    """Загружает и масштабирует изображение."""
    return pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)


# === Фон ===
background = load_scaled_image("fon.png", (WIN_W, WIN_H))

# === Корпус ===
BODY_SIZE = (int(800 * 0.875), int(600 * 0.75))
BODY_POS = (350, 50)
body = load_scaled_image("1.png", BODY_SIZE)

# === Окно микроволновки ===
WINDOW_RECT = pygame.Rect(BODY_POS[0] - 195, BODY_POS[1] - 65, 710, 570)

# === Анимация двери ===
frames_folder = "frames2"
door_frames: list[pygame.Surface] = []

for filename in sort_files_numerically(os.listdir(frames_folder)):
    if filename.endswith(".png"):
        frame_path = os.path.join(frames_folder, filename)
        door_frames.append(
            load_scaled_image(frame_path, (WINDOW_RECT.w, WINDOW_RECT.h))
        )

door_index = 0
door_opening = False
door_closing = False

# === Кнопки ===
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

buttons = []
for name, pos, size in button_data:
    path = os.path.join(buttons_folder, f"{name}.png")
    if os.path.exists(path):
        buttons.append(
            {
                "name": name,
                "image": load_scaled_image(path, size),
                "rect": pygame.Rect(pos, size),
            }
        )


def on_timer():
    print("⏱ Открыт выбор таймера")


def on_frozen():
    print("❄️ Режим разморозки")


def on_double_left():
    print("⏪ Уменьшить время в 2 раза")


def on_left():
    print("◀ Уменьшить время")


def on_ok():
    print("✅ Подтверждение выбора")


def on_right():
    print("▶ Увеличить время")


def on_double_right():
    print("⏩ Увеличить время в 2 раза")


def on_start():
    print("▶ Старт микроволновки")


def on_stop():
    print("⏹ Остановка микроволновки")


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

# === Основной цикл ===
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # Проверка клика по двери
            if WINDOW_RECT.collidepoint(mouse_x, mouse_y):
                if door_index == 0:
                    door_opening, door_closing = True, False
                elif door_index == len(door_frames) - 1:
                    door_closing, door_opening = True, False

            # Проверка клика по кнопкам
            for btn in buttons:
                if btn["rect"].collidepoint(mouse_x, mouse_y):
                    action = button_actions.get(btn["name"])
                    if action:
                        action()

    # === Анимация двери ===
    if door_opening:
        door_index = min(door_index + 1, len(door_frames) - 1)
        if door_index == len(door_frames) - 1:
            door_opening = False
    elif door_closing:
        door_index = max(door_index - 1, 0)
        if door_index == 0:
            door_closing = False

    # === Отрисовка ===
    WIN.blit(background, (0, 0))
    WIN.blit(body, BODY_POS)
    WIN.blit(door_frames[door_index], WINDOW_RECT.topleft)

    for btn in buttons:
        WIN.blit(btn["image"], btn["rect"].topleft)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
