import pygame
from os import path
from random import choice
from sys import exit

# Задаём Размер окна и частоту кадров
WIDTH: int = 750
HEIGHT: int = 650
FPS: int = 20

# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
key_group = pygame.sprite.Group()
key_star_group = pygame.sprite.Group()
life_group = pygame.sprite.Group()

# Задаём основные переменные работы программы
faced_bool: bool = False
win_bool: bool = False
stop_bool: bool = False

key_coord = [[675, 125], [125, 125], [125, 525], [575, 475]]
sea_star_coord = choice([[625, 625], [725, 625]])
key_star_coord = [[675, 625], [675, 325], [225, 75], [475, 325]]

# Создаём матрицу
matrix = [['' for _ in range(15)] for i in range(13)]
KEY: bool = False
KEY_STAR: bool = False


# Функция выключает программу
def terminate():
    # Выключает pygame
    pygame.quit()
    # Выключает всю программу
    exit()


def win():  # функция победы
    global win_bool  # переменная отвечающая за работоспособность спрайтов
    win_bool = True  # При win_bool равном правде все спрайты останавливаются

    font = pygame.font.Font(None, 50)
    text = font.render("Вы выиграли", True, 'white')
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, '#00ae1f', (text_x - 10, text_y - 10,
                                         text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))

    font = pygame.font.Font(None, 30)
    text = font.render("Нажмите пробел, чтобы продолжить", True, 'white')
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT - text.get_height() - 10
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, '#00ae1f', (text_x - 10, text_y - 10,
                                         text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


def return_back():  # Возвращение спрайтов на исходные позиции
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
    if life.give_life() < 0:  # Обнуление очков при нехватке жизней
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


def faced():  # Игрок проиграл, отображение надписи
    global faced_bool
    faced_bool = True

    font = pygame.font.Font(None, 50)
    text = font.render("Игра окончена", True, 'white')
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (255, 4, 86), (text_x - 10, text_y - 10,
                                            text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))

    font = pygame.font.Font(None, 30)
    text = font.render("Нажмите пробел, чтобы продолжить", True, 'white')
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT - text.get_height() - 10
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (255, 4, 86), (text_x - 10, text_y - 10,
                                            text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


def load_image(name, color_key=None):  # Функция для получения фотографий
    fullname = path.join(name)
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


class Shark(pygame.sprite.Sprite):  # Класс акулы
    def __init__(self, sheet, columns, rows, x, y, speed, status, your_list: list = []):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image.set_colorkey('red')
        self.rect = self.rect.move(x, y)
        self.SPEED = speed
        self.status = status
        self.spi = your_list

        if not self.spi:
            self.spi = [sheet, columns, rows, x, y, speed, status]

        else:
            self.spi = your_list

    def cut_sheet(self, sheet, columns, rows):  # получение изображения
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)

        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):  # движение акул, изменение изображения
        global shark_up_image
        global shark_down_image
        global shark_right_image
        global shark_left_image

        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.image.set_colorkey('red')

        if self.status == 1:
            self.rect.y += self.SPEED
            if self.rect.y >= HEIGHT - 150:
                self.__init__(shark_right_image, 2, 1, 0, HEIGHT - 100, 5, 4, self.spi)

        elif self.status == 3:
            self.rect.y -= self.SPEED
            if self.rect.y <= 25:
                self.__init__(shark_left_image, 2, 1, WIDTH - 75, 0, 5, 2, self.spi)

        elif self.status == 2:
            self.rect.x -= self.SPEED
            if self.rect.x <= 0:
                self.__init__(shark_down_image, 4, 1, 0, 0, 5, 1, self.spi)

        elif self.status == 4:
            self.rect.x += self.SPEED
            if self.rect.x >= WIDTH - 100:
                self.__init__(shark_up_image, 4, 1, WIDTH - 50, HEIGHT - 150, 5, 3, self.spi)

        elif self.status == 5:
            self.rect.y -= self.SPEED
            if self.rect.y == 150:
                self.__init__(shark_right_image, 2, 1, 200, 150, 5, 6, self.spi)

        elif self.status == 6:
            self.rect.x += self.SPEED
            if self.rect.x == 450:
                self.__init__(shark_down_image, 4, 1, 500, 150, 5, 7, self.spi)

        elif self.status == 7:
            self.rect.y += self.SPEED
            if self.rect.y == 350:
                self.__init__(shark_left_image, 2, 1, 450, 400, 5, 8, self.spi)

        elif self.status == 8:
            self.rect.x -= self.SPEED
            if self.rect.x == 195:
                self.__init__(shark_up_image, 4, 1, 200, 350, 5, 5, self.spi)

        if pygame.sprite.collide_mask(self, player):
            faced()

    def reloaded(self):  # возвращение на исходную позицию
        self.__init__(*self.spi)


class SeaStar(pygame.sprite.Sprite):  # Класс морской звезды (очки)
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = sea_star_image
        self.image.set_colorkey('green')
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.hide = False
        self.collected = False

    def update(self):
        if not self.hide:  # Исчезновение звезды
            if self.image == white_image:
                self.image = sea_star_image
                self.image.set_colorkey('green')

            if pygame.sprite.collide_mask(self, player):
                self.adding_points()
                self.collected = True

    def adding_points(self):  # добавление очков
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


class Star(pygame.sprite.Sprite):  # Класс звезды
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = white_image
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.hide = True
        self.collected = False

    def update(self):
        if not self.hide:  # Исчезновение звезды
            if self.image == white_image:
                self.image = star_image
                self.image.set_colorkey('green')

            if pygame.sprite.collide_mask(self, player):
                self.adding_points()

    def adding_points(self):  # добавление очков
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
    def __init__(self, need_screen, points: int = 0,
                 color=(237, 28, 36)):  # При создании объекта класса надо задать счёт и цвет очков
        self.points = str(points).rjust(6, '0')  # Создаю переменную очки в которую надо записывать счёт
        self.screen = need_screen
        self.color = color
        self.font = pygame.font.Font(None, 45)
        self.status = 1

    # Функция получает количество очков полученных при собирании звёздочки
    # Если очков выходит больше тысячи прибавляет жизнь
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

    def discharge(self):  # обнуление счета
        self.points = '000000'


def rendering(need_screen, coordinates):
    j, i = coordinates
    j //= 50
    i //= 50
    for y in range(HEIGHT // 50):
        for x in range(WIDTH // 50):
            if not (abs(y - j) <= 1 and abs(x - i) <= 1):
                pygame.draw.rect(need_screen, 'black', (x * 50, y * 50, 50, 50))


class Coral(pygame.sprite.Sprite):  # Класс коралла (преграда)
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        matrix[y // 50][x // 50] = 'Coral'
        self.image = coral_image
        self.image.set_colorkey('green')
        self.rect = self.image.get_rect()
        self.rect.center = x, y


class Key(pygame.sprite.Sprite):  # Класс Ключа для открывания двери
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

    def bring_key(self):  # функция для собирания ключа
        global KEY
        KEY = True
        self.rect.x = 625
        self.rect.y = 0

    def reloaded(self):
        global key_coord
        self.__init__(choice(key_coord))


class KeyStar(pygame.sprite.Sprite):  # Класс ключа для открытия звезд
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

    def bring_key(self):  # Функция при собирании ключа, показывает потайные звезды
        global KEY_STAR
        KEY_STAR = True

        self.rect.x = 575
        self.rect.y = 0
        star.change_hide()
        star1.change_hide()
        star2.change_hide()

    def reloaded(self):
        global key_star_coord
        self.__init__(choice(key_star_coord))


class Door(pygame.sprite.Sprite):  # Класс двери
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


class Player(pygame.sprite.Sprite):  # Класс игрока
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image
        self.image.set_colorkey('white')

        self.rect = self.image.get_rect()
        self.rect.center = WIDTH / 2, HEIGHT - 25

    def get_rects(self):  # функция для получения координат
        return self.rect.y, self.rect.x

    def go_up(self):  # шаг вверх
        self.image = player_image
        self.image.set_colorkey('white')
        if self.rect.y == 0:
            pass

        else:
            y = (self.rect.y - 50) // 50
            if matrix[y][self.rect.x // 50] != 'Coral':
                self.rect.y -= 50

    def go_down(self):  # шаг вниз
        self.image = player_down_image
        self.image.set_colorkey('white')
        if self.rect.y == HEIGHT - 50:
            pass

        else:
            y = (self.rect.y + 50) // 50
            if matrix[y][self.rect.x // 50] != 'Coral':
                self.rect.y += 50

    def go_right(self):  # шаг вправо
        self.image = player_right_image
        self.image.set_colorkey('white')
        if self.rect.x == WIDTH - 50:
            if matrix[self.rect.y // 50][0] != 'Coral':
                self.rect.x = 0

        else:
            x = (self.rect.x + 50) // 50
            if matrix[self.rect.y // 50][x] != 'Coral':
                self.rect.x += 50

    def go_left(self):  # шаг влево
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


class Life(pygame.sprite.Sprite):  # Класс жизни
    def __init__(self, need_screen, color=(237, 28, 36)):
        pygame.sprite.Sprite.__init__(self)

        self.COORDINATS = 675, 25
        self.image = heart_image
        self.image.set_colorkey("green")
        self.rect = self.image.get_rect()
        self.rect.center = 725, 25

        self.screen = need_screen
        self.color = color
        self.font = pygame.font.Font(None, 55)

        self.life = '5'

    def update(self, color=(237, 28, 36)):  # Этот метод позволит обновлять жизни
        text = self.font.render(self.life, True, color)  # Отображение количества жизней
        text_x = 675
        text_y = 10
        screen.blit(text, (text_x, text_y))

    def take_away_life(self):  # При смерти игрока жизнь отнимается
        self.life = str(int(self.life) - 1)

    def give_life(self):  # Получение количества жизни
        return int(self.life)

    def alive(self):  # Для перезапуска уровня
        self.life = '5'


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Adventure experience")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

score = Score(screen)

white_image = load_image('data/white.png')

heart_image = load_image('data/heart.png')
life = Life(screen, score)

life_group.add(life)

all_sprites.add(life)

opening_door_image = load_image('data/opening_door.png')
closing_door_image = load_image('data/closing_door.png')
door = Door(375, 275)

all_sprites.add(door)

sea_star_image = load_image('data/sea_star.png')
sea_star1 = SeaStar(sea_star_coord[0], sea_star_coord[1])
sea_star2 = SeaStar(625, 225)
sea_star3 = SeaStar(75, 175)
sea_star4 = SeaStar(175, 625)

all_sprites.add(sea_star1)
all_sprites.add(sea_star2)
all_sprites.add(sea_star3)
all_sprites.add(sea_star4)

key_star_image = load_image('data/key_star.png')
key_star = KeyStar(choice(key_star_coord))

all_sprites.add(key_star)
key_star_group.add(key_star)

star_image = load_image('data/stars.png')
star = Star(75, 425)
star1 = Star(475, 525)
star2 = Star(275, 275)

all_sprites.add(star)
all_sprites.add(star1)
all_sprites.add(star2)

key_image = load_image('data/key.png')
key = Key(choice(key_coord))

player_image = load_image('data/aqualunger.png')
player_left_image = load_image('data/aqualunger_left.png')
player_right_image = load_image('data/aqualunger_right.png')
player_down_image = load_image('data/aqualunger_down.png')
player = Player()

all_sprites.add(player)
all_sprites.add(key)
key_group.add(key)

shark_up_image = load_image("data/shark_up.png")
shark_down_image = load_image("data/shark_down.png")
shark_left_image = load_image("data/shark_left.png")
shark_right_image = load_image("data/shark_right.png")

shark1 = Shark(shark_up_image, 4, 1, WIDTH - 50, 475, 7, 3, [])
shark2 = Shark(shark_down_image, 4, 1, 0, 80, 7, 1, [])
shark3 = Shark(shark_down_image, 4, 1, 0, 500, 7, 1, [])
shark4 = Shark(shark_up_image, 4, 1, WIDTH - 50, 10, 7, 3, [])
shark5 = Shark(shark_left_image, 2, 1, 325, 0, 7, 2, [])
shark6 = Shark(shark_right_image, 2, 1, 300, HEIGHT - 100, 7, 4, [])
shark7 = Shark(shark_up_image, 4, 1, 200, 250, 5, 5, [])
shark8 = Shark(shark_down_image, 4, 1, 500, 250, 5, 7, [])
shark9 = Shark(shark_left_image, 2, 1, 310, 400, 5, 8, [])
shark10 = Shark(shark_right_image, 2, 1, 320, 150, 5, 6, [])

coral_image = load_image('data/coral.png')
coral1 = Coral(75, 75)
coral2 = Coral(325, 75)
coral3 = Coral(375, 75)
coral4 = Coral(425, 75)
coral5 = Coral(475, 75)
coral6 = Coral(525, 75)
coral7 = Coral(375, 125)
coral8 = Coral(625, 125)
coral9 = Coral(575, 275)
coral10 = Coral(575, 325)
coral11 = Coral(525, 475)
coral12 = Coral(525, 525)
coral13 = Coral(575, 525)
coral14 = Coral(625, 525)
coral15 = Coral(475, 625)
coral16 = Coral(25, 625)
coral17 = Coral(75, 625)
coral18 = Coral(75, 525)
coral19 = Coral(125, 425)
coral20 = Coral(125, 375)
coral21 = Coral(175, 425)
coral22 = Coral(175, 525)
coral23 = Coral(75, 225)
coral24 = Coral(125, 225)
coral25 = Coral(175, 225)
coral26 = Coral(425, 275)
coral27 = Coral(275, 375)
coral28 = Coral(325, 625)
coral29 = Coral(175, 475)
coral30 = Coral(375, 475)
coral31 = Coral(425, 375)
coral32 = Coral(475, 375)
coral33 = Coral(525, 625)
coral34 = Coral(625, 425)
coral35 = Coral(75, 275)
coral36 = Coral(75, 125)
coral37 = Coral(125, 75)
coral38 = Coral(425, 125)
coral39 = Coral(475, 275)
coral40 = Coral(175, 75)
coral41 = Coral(125, 275)
coral42 = Coral(125, 625)
coral43 = Coral(225, 475)
coral44 = Coral(225, 525)
coral45 = Coral(675, 525)
coral46 = Coral(575, 625)
coral47 = Coral(675, 425)
coral48 = Coral(625, 325)
coral49 = Coral(625, 175)
coral50 = Coral(675, 175)
coral51 = Coral(675, 225)
coral52 = Coral(275, 225)

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
all_sprites.add(coral40)
all_sprites.add(coral41)
all_sprites.add(coral42)
all_sprites.add(coral43)
all_sprites.add(coral44)
all_sprites.add(coral45)
all_sprites.add(coral46)
all_sprites.add(coral47)
all_sprites.add(coral48)
all_sprites.add(coral49)
all_sprites.add(coral50)
all_sprites.add(coral51)
all_sprites.add(coral52)


# Цикл игры
def first_level(running: bool = True):

    global KEY
    global KEY_STAR

    global score

    global faced_bool
    global win_bool
    global stop_bool
    life.life='-1'
    return_back()
    faced_bool = False
    win_bool = False
    KEY_STAR = False
    KEY = False

    while running:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if not faced_bool and not win_bool and not stop_bool:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        player.go_up()

                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        player.go_down()

                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        player.go_right()

                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        player.go_left()

                    elif event.key == pygame.K_ESCAPE:
                        stop_bool = True

                elif win_bool:
                    if event.key == pygame.K_SPACE:
                        return score.points

                elif faced_bool:
                    if event.key == pygame.K_SPACE:
                        return_back()
                        faced_bool = False
                        win_bool = False
                        KEY_STAR = False
                        KEY = False

                elif stop_bool:
                    if event.key == pygame.K_ESCAPE:
                        stop_bool = False

        screen.fill((0, 0, 139))
        # Обновление
        if not faced_bool and not win_bool and not stop_bool:
            all_sprites.update()

        all_sprites.draw(screen)
        rendering(screen, player.get_rects())
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
