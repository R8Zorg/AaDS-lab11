import sys

import pygame
from pygame import Surface
from pygame.event import Event

from food import Food, ImageInfo
from microwave import Microwave
from utils import fetch_resource, load_scaled_image


def to_image_info_list(directory: str, states: list[str]) -> list[ImageInfo]:
    return [ImageInfo(state, f"{directory}/{state}.png") for state in states]


def draw_food(window: Surface, food_list: list[Food]) -> None:
    for food in food_list:
        food.draw(window)


def is_food_inside(food_list: list[Food]) -> bool:
    for food in food_list:
        if food.is_inside:
            return True
    return False


def render(
    main_window: Surface,
    background: Surface,
    microwave: Microwave,
    door_state: Surface,
    food_list: list[Food],
) -> None:
    main_window.blit(background, (0, 0))
    main_window.blit(microwave.get_body(), microwave.BODY_POSITION)

    microwave.draw_buttons(main_window)
    microwave.draw_timer(main_window)
    microwave.update_door()

    if is_food_inside(food_list):
        draw_food(main_window, food_list)
        microwave.draw_door(main_window)
    else:
        microwave.draw_door(main_window)
        draw_food(main_window, food_list)

    # microwave.draw_door_hitboxes(WINDOW)

    pygame.display.flip()


def main() -> None:
    pygame.init()
    MAIN_WINDOW: Surface = pygame.display.set_mode((1500, 750))
    FPS: int = 45

    pygame.display.set_caption("Микроволновка")
    background: Surface = load_scaled_image(
        fetch_resource("background.png"), MAIN_WINDOW.get_size()
    )

    microwave: Microwave = Microwave()

    default_states: list[str] = ["frozen", "raw", "done", "overheated"]
    popcorn_states: list[str] = ["raw", "done", "overheated"]
    meat = Food(
        to_image_info_list("meat", default_states),
        (350, 250),
        (1100, 260),
        microwave.INSIDE_RECT,
    )
    pizza = Food(
        to_image_info_list("pizza", default_states),
        (350, 250),
        (1100, 370),
        microwave.INSIDE_RECT,
    )
    popcorn = Food(
        to_image_info_list("popcorn", popcorn_states),
        (350, 250),
        (870, 470),
        microwave.INSIDE_RECT,
    )
    egg = Food(
        to_image_info_list("egg", ["raw", "boom"]),
        (350, 250),
        (1100, 480),
        microwave.INSIDE_RECT,
    )
    food_list: list[Food] = [meat, pizza, popcorn, egg]

    clock: pygame.time.Clock = pygame.time.Clock()
    is_running = True
    while is_running:
        event: Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                break
            if any(
                food.handle_event(event, microwave.is_door_closed)
                for food in food_list
            ):
                continue
            else:
                microwave.handle_event(event)
        render(MAIN_WINDOW, background, microwave, microwave._door_state, food_list)
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
