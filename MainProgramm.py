import pygame
import random
import os

WIDTH = 750
HEIGHT = 650
FPS = 30  # Не трогать! На этом всё работает!

game_folder = os.path.dirname(__file__)
data_folder = os.path.join(game_folder, 'data')

faced_bool = False


def faced():  # Отображает надпись и завершает программу
    global faced_bool
    faced_bool = True

    font = pygame.font.Font(None, 50)
    text = font.render("Игра окончена", True, (255, 0, 0))  # Нужно дописать про пробел
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (255, 0, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)


def add_sprite(sprite):
    all_sprites.add(sprite)
    sprites.append(sprite)
    coordinats.append(sprite.COORDINATS)


def return_back():
    for sprite in range(len(sprites)):
        sprites[sprite].rect.x = coordinats[sprite][0]
        sprites[sprite].rect.y = coordinats[sprite][1]


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

        self.COORDINATS = (350, 600)

        self.rect = self.image.get_rect()
        self.rect.center = WIDTH / 2, HEIGHT - 25

        print(self.rect.y)
        print(self.rect.x)

    def update(self):
        pass

    def go_up(self):
        self.image = player_image
        self.image.set_colorkey('green')

        if self.rect.y == 0:
            pass

        else:
            self.rect.y -= 50

    def go_down(self):
        self.image = player_back_image
        self.image.set_colorkey('green')

        if self.rect.y == HEIGHT - 50:
            pass

        else:
            self.rect.y += 50

    def go_right(self):
        self.image = player_right_image
        self.image.set_colorkey('green')

        if self.rect.x >= WIDTH - 50:
            self.rect.x = 0

        else:
            self.rect.x += 50

    def go_left(self):
        self.image = player_left_image
        self.image.set_colorkey('green')

        if self.rect.x <= 0:
            self.rect.x = WIDTH - 50

        else:
            self.rect.x -= 50


class Enemy(pygame.sprite.Sprite):  # Основной класс для врагов
    def __init__(self, x, y, DIRECTION='Right', SPEED=0):
        pygame.sprite.Sprite.__init__(self)

        self.COORDINATS = (x - 25, y - 25)
        self.DIRECTION = DIRECTION
        self.status = 1

        if SPEED == 0:
            self.SPEED = random.randint(5, 7)

        else:
            self.SPEED = SPEED


class Tumbleweed(Enemy):
    def __init__(self, x, y, DIRECTION='Right', SPEED=0):
        Enemy.__init__(self, x, y, DIRECTION, SPEED)
        self.image = tumbleweed_image
        self.image.set_colorkey('white')

        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def update(self):
        if pygame.sprite.collide_mask(self, player):
            faced()

        elif self.rect.x > WIDTH:
            self.rect.x = -50

        else:
            self.rect.x += self.SPEED

        if self.status == 1:
            self.image = tumbleweed_left_image
            self.image.set_colorkey('white')

            self.status = 2

        elif self.status == 2:
            self.image = tumbleweed_back_image
            self.image.set_colorkey('white')

            self.status = 3

        elif self.status == 3:
            self.image = tumbleweed_right_image
            self.image.set_colorkey('white')

            self.status = 4

        else:
            self.image = tumbleweed_image
            self.image.set_colorkey('white')

            self.status = 1


class Bear(Enemy):
    def __init__(self, x, y,
                 DIRECTION='Right',
                 SPEED=0):  # При создании объекта класса, надо указать координаты и направление спрайта
        Enemy.__init__(self, x, y, DIRECTION, SPEED)
        self.image = bear_stand_image
        self.image.set_colorkey('white')

        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def update(self):
        if pygame.sprite.collide_mask(self, player):
            faced()

        elif self.DIRECTION == 'Right':
            if self.rect.x > WIDTH:
                self.rect.x = -50

            else:
                self.bear_go()
                self.rect.x += self.SPEED

        else:
            if self.rect.x < -50:
                self.rect.x = WIDTH + 50

            else:
                self.bear_go()
                self.rect.x -= self.SPEED

    def bear_go(self):
        if self.status == 1:
            self.image = bear_go_image
            self.image.set_colorkey('white')
            self.status = 2

        elif self.status == 2:
            self.image = bear_stand_image
            self.image.set_colorkey('white')
            self.status = 3

        elif self.status == 3:
            self.image = bear_back_image
            self.image.set_colorkey('white')
            self.status = 4

        else:
            self.image = bear_stand_image
            self.image.set_colorkey('white')
            self.status = 1


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Across The Road")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
sprites = []
coordinats = []  # В этой переменной содержаться координаты всех персонажей

player_image = pygame.image.load(os.path.join(data_folder, 'bigger_player.png')).convert()
player_left_image = pygame.image.load(os.path.join(data_folder, 'bigger_left_player.png')).convert()
player_right_image = pygame.image.load(os.path.join(data_folder, 'bigger_right_player.png')).convert()
player_back_image = pygame.image.load(os.path.join(data_folder, 'bigger_back_player.png')).convert()
player = Player()

tumbleweed_image = pygame.image.load(os.path.join(data_folder, 'tumbleweed.png')).convert()
tumbleweed_left_image = pygame.image.load(os.path.join(data_folder, 'tumbleweed_left.png')).convert()
tumbleweed_back_image = pygame.image.load(os.path.join(data_folder, 'tumbleweed_back.png')).convert()
tumbleweed_right_image = pygame.image.load(os.path.join(data_folder, 'tumbleweed_right.png')).convert()

first_tumbleweed = Tumbleweed(0, HEIGHT - 175, 'Right', 6)
first_second_tumbleweed = Tumbleweed(650, HEIGHT - 175, 'Right', 6)
first_third_tumbleweed = Tumbleweed(50, HEIGHT - 175, 'Right', 6)
first_fourth_tumbleweed = Tumbleweed(200, HEIGHT - 175, 'Right', 6)
first_fifth_tumbleweed = Tumbleweed(250, HEIGHT - 175, 'Right', 6)
first_sixth_tumbleweed = Tumbleweed(400, HEIGHT - 175, 'Right', 6)
first_seventh_tumbleweed = Tumbleweed(450, HEIGHT - 175, 'Right', 6)
first_eighth_tumbleweed = Tumbleweed(600, HEIGHT - 175, 'Right', 6)

second_tumbleweed = Tumbleweed(100, HEIGHT - 275, 'Right', 6)
second_second_tumbleweed = Tumbleweed(750, HEIGHT - 275, 'Right', 6)
second_third_tumbleweed = Tumbleweed(150, HEIGHT - 275, 'Right', 6)
second_fourth_tumbleweed = Tumbleweed(300, HEIGHT - 275, 'Right', 6)
second_fifth_tumbleweed = Tumbleweed(350, HEIGHT - 275, 'Right', 6)
second_sixth_tumbleweed = Tumbleweed(500, HEIGHT - 275, 'Right', 6)
second_seventh_tumbleweed = Tumbleweed(550, HEIGHT - 275, 'Right', 6)
second_eighth_tumbleweed = Tumbleweed(700, HEIGHT - 275, 'Right', 6)

bear_stand_image = pygame.image.load(os.path.join(data_folder, 'bear_go.png')).convert()
bear_go_image = pygame.image.load(os.path.join(data_folder, 'bear_stand.png')).convert()
bear_back_image = pygame.image.load(os.path.join(data_folder, 'bear_back.png')).convert()
bear = Bear(0, HEIGHT - 375)

add_sprite(player)
add_sprite(first_tumbleweed)
add_sprite(first_second_tumbleweed)
add_sprite(first_third_tumbleweed)
add_sprite(first_fourth_tumbleweed)
add_sprite(first_fifth_tumbleweed)
add_sprite(first_sixth_tumbleweed)
add_sprite(first_seventh_tumbleweed)
add_sprite(first_eighth_tumbleweed)

add_sprite(second_tumbleweed)
add_sprite(second_second_tumbleweed)
add_sprite(second_third_tumbleweed)
add_sprite(second_fourth_tumbleweed)
add_sprite(second_fifth_tumbleweed)
add_sprite(second_sixth_tumbleweed)
add_sprite(second_seventh_tumbleweed)
add_sprite(second_eighth_tumbleweed)

add_sprite(bear)

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
            if not faced_bool:
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
                    return_back()
                    faced_bool = False

                else:
                    faced()

    # Обновление
    screen.fill((222, 184, 135))

    if not faced_bool:
        all_sprites.update()

    # Рендеринг
    all_sprites.draw(screen)
    # Вывод клетчатого поля
    if faced_bool:
        faced()
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
