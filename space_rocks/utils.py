from pygame.image import load
from pygame.math import Vector2
from random import randrange, randint
from pygame.mixer import Sound
from pygame import Color


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

def load_sound(name):
    path = path = f'space_rocks/assets/sounds/{name}.wav'
    return Sound(path)

def print_text(surface, text, font, place = 0, color=Color("tomato")):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    if place == 0:
        rect.center = Vector2(surface.get_size()) / 2
    else:
        rect.center = (place)

    surface.blit(text_surface, rect)
