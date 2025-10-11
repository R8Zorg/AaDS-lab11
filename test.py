import os
import re

import pygame

pygame.init()

WIN_W, WIN_H = 1200, 600
WIN = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Микроволновка")

background = pygame.image.load("fon.png").convert()
background = pygame.transform.scale(background, (WIN_W, WIN_H))
BG_X, BG_Y = 0, 0

body = pygame.image.load("1.png").convert_alpha()
BODY_W, BODY_H = int(800 * 0.875), int(600 * 0.75)
body = pygame.transform.scale(body, (BODY_W, BODY_H))
BODY_X, BODY_Y = 350, 50

WINDOW_X_ORIG = -195
WINDOW_Y_ORIG = -65
WINDOW_W_ORIG = 710
WINDOW_H_ORIG = 570

WINDOW_X = BODY_X + WINDOW_X_ORIG
WINDOW_Y = BODY_Y + WINDOW_Y_ORIG
WINDOW_W = WINDOW_W_ORIG
WINDOW_H = WINDOW_H_ORIG

door_frames = []
frames_folder = "frames2"


def sort_files_numerically(files):
    return sorted(
        files,
        key=lambda name: [
            int(s) if s.isdigit() else s for s in re.split(r"(\d+)", name)
        ],
    )


for filename in sort_files_numerically(os.listdir(frames_folder)):
    if filename.endswith(".png"):
        path = os.path.join(frames_folder, filename)
        frame = pygame.image.load(path).convert_alpha()
        frame = pygame.transform.scale(frame, (WINDOW_W, WINDOW_H))
        door_frames.append(frame)

door_index = 0
door_opening = False
door_closing = False

buttons = []
buttons_folder = "buttons"

button_data = [
    ("timer.png", (875, 85), (155, 65)),
    ("frozen.png", (875, 167), (150, 60)),
    ("double_left.png", (868, 242), (30, 38)),
    ("left.png", (901, 240), (25, 40)),
    ("ok.png", (930, 240), (40, 40)),
    ("right.png", (975, 240), (25, 40)),
    ("double_right.png", (1005, 240), (30, 40)),
    ("start.png", (897, 300), (100, 60)),
    ("stop.png", (897, 380), (100, 60)),
]

for filename, pos, size in button_data:
    path = os.path.join(buttons_folder, filename)
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, size)
        rect = img.get_rect(topleft=pos)
        buttons.append({"image": img, "rect": rect})

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if (WINDOW_X <= mouse_x <= WINDOW_X + WINDOW_W) and (
                WINDOW_Y <= mouse_y <= WINDOW_Y + WINDOW_H
            ):
                if door_index == 0:
                    door_opening = True
                    door_closing = False
                elif door_index == len(door_frames) - 1:
                    door_closing = True
                    door_opening = False

            for btn in buttons:
                if btn["rect"].collidepoint(mouse_x, mouse_y):
                    pass

    if door_opening:
        if door_index < len(door_frames) - 1:
            door_index += 1
        else:
            door_opening = False

    elif door_closing:
        if door_index > 0:
            door_index -= 1
        else:
            door_closing = False

    WIN.blit(background, (BG_X, BG_Y))
    WIN.blit(body, (BODY_X, BODY_Y))
    WIN.blit(door_frames[door_index], (WINDOW_X, WINDOW_Y))

    for btn in buttons:
        WIN.blit(btn["image"], btn["rect"].topleft)

    pygame.display.update()
    clock.tick(30)

pygame.quit()
