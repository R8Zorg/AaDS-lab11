import pygame


def load_scaled_image(path: str, size: tuple[int, int]) -> pygame.Surface:
    return pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)


def fetch_resource(resource_name: str = "", food: str = "", microwave: str = "") -> str:
    if food:
        return "resources/food/" + food
    elif microwave:
        return "resources/microwave/" + microwave
    else:
        return "resources/" + resource_name
