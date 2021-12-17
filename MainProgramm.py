import pygame
import random
import os

WIDTH = 650
HEIGHT = 650
FPS = 30  # Не трогать! На этом всё работает!

game_folder = os.path.dirname(__file__)
data_folder = os.path.join(game_folder, 'data')

faced = False


class Board:
    def render(self, screen):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                pygame.draw.rect(screen, 'white',
                                 (x * 50, y * 50, 50, 50), 1)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image
        self.image.set_colorkey('green')

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 25)

        print(self.rect.y)
        print(self.rect.x)

    def update(self):
        pass

    def go_up(self):
        if self.rect.y == 0:
            pass

        else:
            self.rect.y -= 50

    def go_down(self):
        if self.rect.y == HEIGHT - 50:
            pass

        else:
            self.rect.y += 50

    def go_right(self):
        if self.rect.x == WIDTH - 50:
            self.rect.x = 0

        else:
            self.rect.x += 50

    def go_left(self):
        if self.rect.x == 0:
            self.rect.x = WIDTH - 50

        else:
            self.rect.x -= 50


class Tumbleweed(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = tumbleweed_image
        self.image.set_colorkey('white')

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = random.randint(5, 8)

    def update(self):
        if pygame.sprite.collide_mask(self, player):
            global faced
            faced = True

        elif self.rect.x > WIDTH:
            self.rect.x = -50

        else:
            self.rect.x += self.speed


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Across The Road")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

player_image = pygame.image.load(os.path.join(data_folder, 'bigger_player.png')).convert()
player = Player()

tumbleweed_image = pygame.image.load(os.path.join(data_folder, 'tumbleweed.png')).convert()
tumbleweed = Tumbleweed(0, HEIGHT - 175)
tumbleweed2 = Tumbleweed(0, HEIGHT - 275)

all_sprites.add(player)
all_sprites.add(tumbleweed)
all_sprites.add(tumbleweed2)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not faced:
                if event.key == pygame.K_w:
                    player.go_up()

                elif event.key == pygame.K_s:
                    player.go_down()

                elif event.key == pygame.K_d:
                    player.go_right()

                elif event.key == pygame.K_a:
                    player.go_left()

            else:
                if event.key == pygame.K_SPACE:
                    running = False

    # Обновление
    screen.fill((222, 184, 135))

    if not faced:
        all_sprites.update()

    # Рендеринг
    all_sprites.draw(screen)
    # Вывод клетчатого поля

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
