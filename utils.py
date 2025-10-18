import pygame


def load_scaled_image(path: str, size: tuple[int, int]) -> pygame.Surface:
    return pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)


def fetch_resource(resource_name: str) -> str:
    return "resources/" + resource_name
