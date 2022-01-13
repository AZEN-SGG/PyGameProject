import pygame
import os
import sys
from random import choice

WIDTH = 650
HEIGHT = 650
FPS = 20

all_sprites = pygame.sprite.Group()
key_group = pygame.sprite.Group()
key_star_group = pygame.sprite.Group()
life_group = pygame.sprite.Group()

game_folder = os.path.dirname(__file__)
data_folder = os.path.join(game_folder, 'data')
faced_bool = False
win_bool = False
key_coord = [[575, 75], [125, 125], [75, 525], [525, 475]]
sea_star_coord = choice([[625, 625], [525, 625]])
key_star_coord = [[575, 625], [575, 325], [225, 75], [375, 325]]

matrix = [['' for _ in range(13)] for i in range(13)]
KEY = False
KEY_STAR = False


def win():
    global win_bool  # переменная отвечающая за работоспособность спрайтов
    win_bool = True  # При win_bool равном правде все спрайты останавливаются

    font = pygame.font.Font(None, 50)
    text = font.render("Вы выиграли", True, 'white')  # Нужно дописать про пробел
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (255, 4, 86), (text_x - 10, text_y - 10,
                                            text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


def return_back():
    life.take_away_life()
    shark1.reloaded()
    shark2.reloaded()
    shark3.reloaded()
    shark4.reloaded()
    shark5.reloaded()
    shark6.reloaded()
    shark7.reloaded()
    shark8.reloaded()
    shark9.reloaded()
    shark10.reloaded()
    player.reloaded()
    key.reloaded()
    key_star.reloaded()
    if life.give_life() < 0 or win_bool:
        score.discharge()
        life.alive()
        star.status_collected()
        star1.status_collected()
        star2.status_collected()
        sea_star1.status_collected()
        sea_star2.status_collected()
        sea_star3.status_collected()
        sea_star4.status_collected()
    star.reloaded()
    star1.reloaded()
    star2.reloaded()
    sea_star1.reloaded()
    sea_star2.reloaded()
    sea_star3.reloaded()
    sea_star4.reloaded()


def faced():  # Отображает надпись и завершает программу
    global faced_bool
    faced_bool = True

    font = pygame.font.Font(None, 50)
    text = font.render("Игра окончена", True, 'white')  # Нужно дописать про пробел
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (255, 4, 86), (text_x - 10, text_y - 10,
                                            text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


def load_image(name, color_key=None):
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


def load_level(filename):
    filename = filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Shark(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, SPEED, status):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image.set_colorkey('red')
        self.rect = self.rect.move(x, y)
        self.SPEED = SPEED
        self.status = status
        self.spi = [sheet, columns, rows, x, y, SPEED, status]

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.image.set_colorkey('red')
        if self.status == 1:
            self.rect.y += self.SPEED
            if self.rect.y >= HEIGHT - 150:
                self.__init__(load_image("data/" + "shark_right.png"), 2, 1, 0, HEIGHT - 100, 5, 4)
        if self.status == 3:
            self.rect.y -= self.SPEED
            if self.rect.y <= 25:
                self.__init__(load_image("data/" + "shark_left.png"), 2, 1, WIDTH - 75, 0, 5, 2)
        if self.status == 2:
            self.rect.x -= self.SPEED
            if self.rect.x <= 0:
                self.__init__(load_image("data/" + "shark_down.png"), 4, 1, 0, 0, 5, 1)
        if self.status == 4:
            self.rect.x += self.SPEED
            if self.rect.x >= WIDTH - 100:
                self.__init__(load_image("data/" + "shark_up.png"), 4, 1, WIDTH - 50, HEIGHT - 150, 5, 3)
        if self.status == 5:
            self.rect.y -= self.SPEED
            if self.rect.y == 150:
                self.__init__(load_image("data/" + "shark_right.png"), 2, 1, 150, 150, 5, 6)
        if self.status == 6:
            self.rect.x += self.SPEED
            if self.rect.x == 400:
                self.__init__(load_image("data/" + "shark_down.png"), 4, 1, 450, 150, 5, 7)
        if self.status == 7:
            self.rect.y += self.SPEED
            if self.rect.y == 350:
                self.__init__(load_image("data/" + "shark_left.png"), 2, 1, 400, 400, 5, 8)
        if self.status == 8:
            self.rect.x -= self.SPEED
            if self.rect.x == 145:
                self.__init__(load_image("data/" + "shark_up.png"), 4, 1, 150, 350, 5, 5)
        if pygame.sprite.collide_mask(self, player):
            faced()

    def reloaded(self):
        self.__init__(*self.spi)


class SeaStar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = sea_star_image
        self.image.set_colorkey('green')
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.hide = False
        self.collected = False

    def update(self):
        if not self.hide:
            if self.image == white_image:
                self.image = sea_star_image
                self.image.set_colorkey('green')

            if pygame.sprite.collide_mask(self, player):
                self.adding_points()
                self.collected = True

    def adding_points(self):
        self.hide = True
        self.collected = True

        self.image = white_image
        self.image.set_colorkey('white')
        score.add_points(500)

    def reloaded(self):
        if not self.collected:
            self.hide = False

    def status_collected(self):
        self.collected = False


class Star(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = white_image
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.hide = True
        self.collected = False

    def update(self):
        if not self.hide:
            if self.image == white_image:
                self.image = star_image
                self.image.set_colorkey('green')

            if pygame.sprite.collide_mask(self, player):
                self.adding_points()

    def adding_points(self):
        self.hide = True
        self.collected = True

        self.image = white_image
        self.image.set_colorkey('white')
        score.add_points(1000)

    def change_hide(self):
        if not self.collected:
            self.hide = False
            self.image = star_image
            self.image.set_colorkey('green')

    def reloaded(self):
        self.hide = True
        self.image = white_image
        self.image.set_colorkey('white')

    def status_collected(self):
        self.collected = False


class Score:  # Класс счёта
    def __init__(self, screen, points: int = 0,
                 color=(237, 28, 36)):  # При создании объекта класса надо задать счёт и цвет очков
        self.points = str(points).rjust(6, '0')  # Создаю переменную очки в которую надо записывать счёт
        self.screen = screen
        self.color = color
        self.font = pygame.font.Font(None, 45)
        self.type = 'Score'  # Задаёт класс
        self.status = 1

    def add_points(self, point):
        self.points = str(int(self.points) + point).rjust(6, '0')

    def update(self, color=(237, 28, 36)):  # Этот метод позволит обновлять счёт
        text = self.font.render(self.points, True, 'yellow')  # Рисую счёт - коричневый цвет
        text_w = text.get_width()
        text_h = text.get_height()
        text_x = 15
        text_y = 15
        pygame.draw.rect(screen, color, (text_x - 5, text_y - 5,
                                         text_w + 10, text_h + 5), 1)
        pygame.draw.rect(screen, color, (text_x - 5, text_y - 5,
                                         text_w + 10, text_h + 5))
        screen.blit(text, (text_x, text_y))

    def discharge(self):
        self.points = '000000'


class Board:
    def render(self, screen, coor):
        j, i = coor
        j //= 50
        i //= 50
        for y in range(HEIGHT // 50):
            for x in range(WIDTH // 50):
                if not (abs(y - j) <= 1 and abs(x - i) <= 1):
                    pygame.draw.rect(screen, 'black', (x * 50, y * 50, 50, 50))
                # pygame.draw.rect(screen, 'white',
                #                (x * 50, y * 50, 50, 50), 1)


class Coral(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        matrix[y // 50][x // 50] = 'Coral'
        self.image = coral_image
        self.image.set_colorkey('green')
        self.rect = self.image.get_rect()
        self.rect.center = x, y


class Key(pygame.sprite.Sprite):
    # При создании объекта класса надо задать координаты, а также есть возможность выбрать уровень
    def __init__(self, coord):
        x, y = coord[0], coord[1]
        pygame.sprite.Sprite.__init__(self)  # Переменная отвечает за показывание картинки
        self.image = key_image
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def update(self):
        if not KEY:
            if pygame.sprite.collide_mask(self, player):
                self.bring_key()

    def bring_key(self):
        global KEY
        KEY = True
        self.rect.x = 525
        self.rect.y = 0

    def reloaded(self):
        global key_coord
        self.__init__(choice(key_coord))


class KeyStar(pygame.sprite.Sprite):
    # При создании объекта класса надо задать координаты, а также есть возможность выбрать уровень
    def __init__(self, coord):
        x, y = coord[0], coord[1]
        pygame.sprite.Sprite.__init__(self)  # Переменная отвечает за показывание картинки
        self.image = key_star_image
        self.image.set_colorkey('green')
        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def update(self):
        if pygame.sprite.collide_mask(self, player):
            self.bring_key()

    def bring_key(self):
        global KEY_STAR
        KEY_STAR = True

        self.rect.x = 475
        self.rect.y = 0
        star.change_hide()
        star1.change_hide()
        star2.change_hide()

    def reloaded(self):
        global key_star_coord
        self.__init__(choice(key_star_coord))


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = closing_door_image
        self.image.set_colorkey('green')
        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def update(self):
        if KEY:
            self.image = opening_door_image
            self.image.set_colorkey('green')
            if pygame.sprite.collide_mask(self, player):
                win()
        else:
            self.image = closing_door_image
            self.image.set_colorkey('green')


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image
        self.image.set_colorkey('white')

        self.rect = self.image.get_rect()
        self.rect.center = WIDTH / 2, HEIGHT - 25

    def get_rects(self):
        return self.rect.y, self.rect.x

    def update(self):
        pass

    def go_up(self):
        self.image = player_image
        self.image.set_colorkey('white')
        if self.rect.y == 0:
            pass
        else:
            y = (self.rect.y - 50) // 50
            if matrix[y][self.rect.x // 50] != 'Coral':
                self.rect.y -= 50

    def go_down(self):
        self.image = player_down_image
        self.image.set_colorkey('white')
        if self.rect.y == HEIGHT - 50:
            pass
        else:
            y = (self.rect.y + 50) // 50
            if matrix[y][self.rect.x // 50] != 'Coral':
                self.rect.y += 50

    def go_right(self):
        self.image = player_right_image
        self.image.set_colorkey('white')
        if self.rect.x == WIDTH - 50:
            self.rect.x = 0

        else:
            x = (self.rect.x + 50) // 50
            if matrix[self.rect.y // 50][x] != 'Coral':
                self.rect.x += 50

    def go_left(self):
        self.image = player_left_image
        self.image.set_colorkey('white')
        if self.rect.x == 0:
            self.rect.x = WIDTH - 50

        else:
            x = (self.rect.x - 50) // 50
            if matrix[self.rect.y // 50][x] != 'Coral':
                self.rect.x -= 50

    def reloaded(self):
        self.image = player_image
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH / 2, HEIGHT - 25


class Life(pygame.sprite.Sprite):

    def __init__(self, screen, color=(237, 28, 36)):
        pygame.sprite.Sprite.__init__(self)

        self.COORDINATS = 575, 25
        self.image = heart_image
        self.image.set_colorkey("green")
        self.rect = self.image.get_rect()
        self.rect.center = 625, 25

        self.screen = screen
        self.color = color
        self.font = pygame.font.Font(None, 55)

        self.life = '3'

    def update(self, color=(237, 28, 36)):  # Этот метод позволит обновлять счёт
        text = self.font.render(self.life, True, color)  # Рисую счёт - коричневый цвет
        text_x = 575
        text_y = 10
        screen.blit(text, (text_x, text_y))

    def take_away_life(self):
        self.life = str(int(self.life) - 1)

    def give_life(self):
        return int(self.life)

    def alive(self):
        self.life = '3'


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Adventure experience")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

score = Score(screen)

all_sprites = pygame.sprite.Group()

white_image = pygame.image.load(os.path.join(data_folder, 'white.png')).convert()

board = Board()

heart_image = pygame.image.load(os.path.join(data_folder, 'heart.png')).convert()
life = Life(screen, score)

life_group.add(life)

all_sprites.add(life)

opening_door_image = pygame.image.load(os.path.join(data_folder, 'opening_door.png')).convert()
closing_door_image = pygame.image.load(os.path.join(data_folder, 'closing_door.png')).convert()
door = Door(325, 275)

sea_star_image = pygame.image.load(os.path.join(data_folder, 'sea_star.png')).convert()
sea_star1 = SeaStar(sea_star_coord[0], sea_star_coord[1])
sea_star2 = SeaStar(575, 225)
sea_star3 = SeaStar(75, 175)
sea_star4 = SeaStar(125, 625)

all_sprites.add(sea_star1)
all_sprites.add(sea_star2)
all_sprites.add(sea_star3)
all_sprites.add(sea_star4)

key_star_image = pygame.image.load(os.path.join(data_folder, 'key_star.png')).convert()
key_star = KeyStar(choice(key_star_coord))

all_sprites.add(key_star)
key_star_group.add(key_star)

star_image = pygame.image.load(os.path.join(data_folder, 'stars.png')).convert()
star = Star(75, 425)
star1 = Star(425, 525)
star2 = Star(225, 275)

all_sprites.add(star)
all_sprites.add(star1)
all_sprites.add(star2)

key_image = pygame.image.load(os.path.join(data_folder, 'key.png')).convert()
key = Key(choice(key_coord))

player_image = pygame.image.load(os.path.join(data_folder, 'aqualunger.png')).convert()
player_left_image = pygame.image.load(os.path.join(data_folder, 'aqualunger_left.png')).convert()
player_right_image = pygame.image.load(os.path.join(data_folder, 'aqualunger_right.png')).convert()
player_down_image = pygame.image.load(os.path.join(data_folder, 'aqualunger_down.png')).convert()
player = Player()

all_sprites.add(player)
all_sprites.add(key)
key_group.add(key)

shark1 = Shark(load_image("data/" + "shark_up.png"), 4, 1, WIDTH - 50, 475, 7, 3)
shark2 = Shark(load_image("data/" + "shark_down.png"), 4, 1, 0, 80, 7, 1)
shark3 = Shark(load_image("data/" + "shark_down.png"), 4, 1, 0, 500, 7, 1)
shark4 = Shark(load_image("data/" + "shark_up.png"), 4, 1, WIDTH - 50, 50, 7, 3)
shark5 = Shark(load_image("data/" + "shark_left.png"), 2, 1, 275, 0, 7, 2)
shark6 = Shark(load_image("data/" + "shark_right.png"), 2, 1, 300, HEIGHT - 100, 7, 4)
shark7 = Shark(load_image("data/" + "shark_up.png"), 4, 1, 150, 250, 5, 5)
shark8 = Shark(load_image("data/" + "shark_down.png"), 4, 1, 450, 250, 5, 7)
shark9 = Shark(load_image("data/" + "shark_left.png"), 2, 1, 260, 400, 5, 8)
shark10 = Shark(load_image("data/" + "shark_right.png"), 2, 1, 270, 150, 5, 6)

coral_image = pygame.image.load(os.path.join(data_folder, 'coral.png')).convert()
coral1 = Coral(75, 75)
coral2 = Coral(275, 75)
coral3 = Coral(325, 75)
coral4 = Coral(375, 75)
coral5 = Coral(425, 75)
coral6 = Coral(475, 75)
coral7 = Coral(375, 125)
coral8 = Coral(575, 175)
coral9 = Coral(525, 275)
coral10 = Coral(525, 325)
coral11 = Coral(475, 475)
coral12 = Coral(475, 525)
coral13 = Coral(525, 525)
coral14 = Coral(575, 525)
coral15 = Coral(425, 625)
coral16 = Coral(25, 625)
coral17 = Coral(75, 625)
coral18 = Coral(125, 525)
coral19 = Coral(125, 475)
coral20 = Coral(125, 425)
coral21 = Coral(125, 375)
coral22 = Coral(175, 525)
coral23 = Coral(75, 225)
coral24 = Coral(125, 225)
coral25 = Coral(225, 225)
coral26 = Coral(425, 275)
coral27 = Coral(225, 375)
coral28 = Coral(275, 625)
coral29 = Coral(175, 475)
coral30 = Coral(325, 475)
coral31 = Coral(375, 375)
coral32 = Coral(425, 375)
coral33 = Coral(475, 625)
coral34 = Coral(575, 425)
coral35 = Coral(75, 275)
coral36 = Coral(75, 125)
coral37 = Coral(125, 75)
coral38 = Coral(325, 125)
coral39 = Coral(375, 275)

all_sprites.add(coral1)
all_sprites.add(coral2)
all_sprites.add(coral3)
all_sprites.add(coral4)
all_sprites.add(coral5)
all_sprites.add(coral6)
all_sprites.add(coral7)
all_sprites.add(coral8)
all_sprites.add(coral9)
all_sprites.add(coral10)
all_sprites.add(coral11)
all_sprites.add(coral12)
all_sprites.add(coral13)
all_sprites.add(coral14)
all_sprites.add(coral15)
all_sprites.add(coral16)
all_sprites.add(coral17)
all_sprites.add(coral18)
all_sprites.add(coral19)
all_sprites.add(coral20)
all_sprites.add(coral21)
all_sprites.add(coral22)
all_sprites.add(coral23)
all_sprites.add(coral24)
all_sprites.add(coral25)
all_sprites.add(coral26)
all_sprites.add(coral27)
all_sprites.add(coral28)
all_sprites.add(coral29)
all_sprites.add(coral30)
all_sprites.add(coral31)
all_sprites.add(coral32)
all_sprites.add(coral33)
all_sprites.add(coral34)
all_sprites.add(coral35)
all_sprites.add(coral36)
all_sprites.add(coral37)
all_sprites.add(coral38)
all_sprites.add(coral39)

all_sprites.add(door)
# Цикл игры
running = True


def second_level(running):
    global KEY
    global KEY_STAR
    global faced_bool
    global win_bool

    while running:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if not faced_bool and not win_bool:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        player.go_up()

                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        player.go_down()

                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        player.go_right()

                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        player.go_left()
                elif win_bool:
                    if event.key == pygame.K_SPACE:
                        running=False
                else:
                    if event.key == pygame.K_SPACE:
                        return_back()
                        faced_bool = False
                        win_bool = False
                        KEY_STAR = False
                        KEY = False

        screen.fill((0, 0, 139))
        # Обновление
        if not faced_bool and not win_bool:
            all_sprites.update()
        all_sprites.draw(screen)
        board.render(screen, player.get_rects())
        score.update()
        life_group.update()
        life_group.draw(screen)
        if KEY:
            key_group.draw(screen)
        if KEY_STAR:
            key_star_group.draw(screen)
        if faced_bool:
            faced()
        if win_bool:
            win()
        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()
