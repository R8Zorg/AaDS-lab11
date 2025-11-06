import pygame
from PIL import Image


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


def load_image(path: str, target_size: tuple[int, int]) -> pygame.Surface:
    image: Image = Image.open(path).convert("RGB")
    image = image.resize(target_size, Image.LANCZOS)

    mode = image.mode
    size = image.size
    data = image.tobytes()
    return pygame.image.fromstring(data, size, mode)
