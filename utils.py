import pygame


def load_scaled_image(path: str, size: tuple[int, int]) -> pygame.Surface:
    return pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)


def fetch_resource(resource_name: str = "", food: str = "", microwave: str = "") -> str:
    resources_folder: str = "resources"
    if food:
        return f"{resources_folder}/food/" + food
    elif microwave:
        return f"{resources_folder}/microwave/" + microwave
    else:
        return f"{resources_folder}/" + resource_name
