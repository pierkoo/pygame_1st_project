from pygame.image import load
from pygame.math import Vector2
from random import randrange, randint


def load_sprite(name, with_alpha=True):
    path = f'space_rocks/assets/sprites/{name}.png'
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()

def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)

def get_random_position(surface):
    return Vector2(
        randrange(surface.get_width()),
        randrange(surface.get_height()),
    )

def get_random_velocity(min_speed, max_speed):
    speed = randint(min_speed, max_speed)
    angle = randrange(0, 360)
    return Vector2(speed,0).rotate(angle)
