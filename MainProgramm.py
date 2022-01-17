import ThirdLevel
import FirstLevel
import SecondLevel

import pygame
import sys
import os

WIDTH = 750
HEIGHT = 650
FPS = 20


def load_image(name, color_key=None):
    name = "data/" + name
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()





pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Adventure experience")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

something = FirstLevel.first_level(True)

if something is not None:
    level = int(something[1])
    hearts = something[2]
    points = something[3]

    if level == 1:
        something = FirstLevel.first_level(True, hearts, points)

    elif level == 2:
        something = SecondLevel.second_level(True, hearts, points)

    else:
        something = ThirdLevel.third_level(True, hearts, points)

else:
    something = SecondLevel.second_level(True)

something = ThirdLevel.third_level(True)



pygame.quit()
