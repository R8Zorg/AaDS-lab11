import pygame
from pygame import Surface

from app import App
from food import Food, FoodState, ImageInfo
from microwave import Microwave


def to_image_info_list(directory: str, states: list[FoodState]) -> list[ImageInfo]:
    return [
        ImageInfo(food_state, f"{directory}/{food_state.state}.png")
        for food_state in states
    ]


def main() -> None:
    pygame.init()
    WINDOW_SIZE = (1500, 750)
    MAIN_WINDOW: Surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Микроволновка")

    microwave: Microwave = Microwave()

    default_food_states: list[FoodState] = [
        FoodState("frozen", 20),
        FoodState("raw", 15),
        FoodState("done", 10),
        FoodState("overheated"),
    ]
    popcorn_states: list[FoodState] = [
        FoodState("raw", 15),
        FoodState("done", 10),
        FoodState("overheated"),
    ]
    meat = Food(
        to_image_info_list("meat", default_food_states),
        (1100, 260),
        microwave.INSIDE_RECT,
    )
    pizza = Food(
        to_image_info_list("pizza", default_food_states),
        (1100, 370),
        microwave.INSIDE_RECT,
    )
    popcorn = Food(
        to_image_info_list("popcorn", popcorn_states),
        (870, 470),
        microwave.INSIDE_RECT,
    )
    egg = Food(
        to_image_info_list("egg", [FoodState("raw", 15), FoodState("boom")]),
        (1100, 480),
        microwave.INSIDE_RECT,
    )

    app: App = App(
        MAIN_WINDOW, "background.png", microwave, [meat, pizza, popcorn, egg]
    )
    app.run()


if __name__ == "__main__":
    main()
