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


def start_screen(intro_text):
    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50

    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.flip()
        clock.tick(FPS)


intro_text = ["Первый Уровень - Уровень Риты",
              "#to do: Написать правила к каждому уровню и придумать название"]

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Adventure experience")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

start_screen(intro_text)

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
