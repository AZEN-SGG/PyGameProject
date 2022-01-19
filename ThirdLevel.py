import pygame
from sys import exit
from random import randint
from os import path

WIDTH: int = 750
HEIGHT: int = 650
FPS: int = 30  # Не трогать! На этом всё работает!

game_folder = path.dirname(__file__)
data_folder = path.join(game_folder, 'data')

state_points: str = '000000'

faced_bool: bool = False
win_bool: bool = False
stop_bool: bool = False

matrix: list = []

life_group = pygame.sprite.Group()


# Функция проигрыши, запускается при проигрыше
def faced(heart):  # Отображает надпись и завершает программу
    global faced_bool
    faced_bool = True

    if heart.life == '0':
        font = pygame.font.Font(None, 50)
        text = font.render("Игра окончена", True, (255, 0, 0))  # Нужно дописать про пробел
        text_x = WIDTH // 2 - text.get_width() // 2
        text_y = HEIGHT // 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (255, 0, 0), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 1)

    else:
        font = pygame.font.Font(None, 50)
        text = font.render("Вы проиграли", True, (255, 0, 0))  # Нужно дописать про пробел
        text_x = WIDTH // 2 - text.get_width() // 2
        text_y = HEIGHT // 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (255, 0, 0), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 1)


def load_image(image: str):
    return pygame.image.load(path.join(data_folder, image)).convert()


# Функция отвечает за запись рекордов, которые происходят при выигрыше последнего третьего уровня
def record():
    global score

    points = score.points

    # Открываем файл с рекордами
    with open('record.txt', 'r', encoding='utf8') as file:
        # Берём оттуда текст
        text = file.readlines()

    # Закрываем файл
    file.close()

    # Превращаем текст в список построчно
    text = [int(x) for x in text]
    # Добавляем наш рекорд в список
    text.append(int(points))
    # Сортируем список по возрастанию
    text.sort(reverse=True)
    # Удаляем все элементы до оставшихся трёх самых больших рекордов
    text = text[:3]

    records: str = ''

    # Открываем файл для записи
    file = open("record.txt", 'w')
    # Записываем поэлементно
    for element in text:
        records += str(element).rjust(6, '0') + '\n'

    records: str = records.rstrip('\n')
    file.write(records)

    # Закрываем файл
    file.close()

    records: list = records.split('\n')
    records.append(points)

    return records


# Функция выключает программу
def terminate():
    # Выключает pygame
    pygame.quit()
    # Выключает всю программу
    exit()


# Отображает сообщение о выигрыше
def win():
    global win_bool  # переменная отвечающая за работоспособность спрайтов
    win_bool = True  # При win_bool равном правде все спрайты останавливаются

    font = pygame.font.Font(None, 50)
    text = font.render("Вы выиграли", True, (0, 255, 0))  # Нужно дописать про пробел
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)


def add_sprite(sprite):  # Добавление спрайтов
    all_sprites.add(sprite)  # Обновление спрайтов
    sprites.append(sprite)  # Добавляет в одну папку все спрайты
    coordinates.append(sprite.COORDINATES)  # Координаты

    type = sprite.type

    # Если класс не равен: Пуле, Перекати поел и Жизням, то добавляем в матрицу
    if type != 'Bullet' and type != 'Tumbleweed' and type != 'Life':
        x = sprite.COORDINATES[0] // 50
        y = sprite.COORDINATES[1] // 50

        matrix[y][x] = sprite.type


def return_back():  # Поражение -> возвращение назад
    for sprite in range(len(sprites)):
        sprites[sprite].rect.x = coordinates[sprite][0]
        sprites[sprite].rect.y = coordinates[sprite][1]
        sprites[sprite].status = 1

        if sprites[sprite].type == 'Point':  # Мешочек с золотом
            sprites[sprite].hide = False
            score.points = state_points

        elif sprites[sprite].type == 'Key':
            sprites[sprite].hide = False

        elif sprites[sprite].type == 'Bullet':  # Пулька
            sprites[sprite].delay = sprites[sprite].INITIAL_DELAY
            sprites[sprite].image = white_image
            sprites[sprite].image.set_colorkey('white')


# При вызове функции можно задать количество очков которые прибавляются в счёту
def get_point(this_point, add_points: int = 500):
    this_point.hide = True
    points = str(int(score.points) + add_points)

    if len(points) < 6:
        points = '0' * (6 - len(points)) + points

    score.points = points
    score.update()


# Функция создаёт матрицу
def make_matrix():
    for y in range(13):
        matrix.append([])
        for x in range(15):
            matrix[y].append('')


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.status = 1
        self.image = player_image
        self.image.set_colorkey('green')
        self.type = 'Player'

        self.COORDINATES = (350, 600)

        self.rect = self.image.get_rect()
        self.rect.center = WIDTH / 2, HEIGHT - 25

    def update(self):
        if self.status == 1:
            self.image = player_image
            self.image.set_colorkey('green')

    def go_into_bush(self, direction):
        if direction == 'Right':
            self.status = 3
            self.image = player_right_image
            self.image.set_colorkey('green')

            if self.rect.x >= WIDTH - 50:
                if matrix[self.rect.y // 50][0] != 'Hedge':
                    self.rect.x = 0

            else:
                if matrix[self.rect.y // 50][self.rect.x // 50 + 1] != 'Hedge':
                    self.rect.x += 50

        elif direction == 'Left':
            self.status = 4
            self.image = player_left_image
            self.image.set_colorkey('green')

            if self.rect.x <= 0:
                if matrix[self.rect.y // 50][14] != 'Hedge':
                    self.rect.x = WIDTH - 50

            else:
                if matrix[self.rect.y // 50][self.rect.x // 50 - 1] != 'Hedge':
                    self.rect.x -= 50

        elif direction == 'Up':
            self.status = 1
            self.image = player_image
            self.image.set_colorkey('green')

            if self.rect.y == 0:
                win()

            else:
                if matrix[self.rect.y // 50 - 1][self.rect.x // 50] != 'Hedge':
                    self.rect.y -= 50

        else:
            self.status = 2
            self.image = player_back_image
            self.image.set_colorkey('green')

            if self.rect.y != HEIGHT - 50:
                if matrix[self.rect.y // 50 + 1][self.rect.x // 50] != 'Hedge':
                    self.rect.y += 50


class Enemy(pygame.sprite.Sprite):  # Основной класс для врагов
    def __init__(self, x, y, direction: str = 'Right', speed: int = 0):
        pygame.sprite.Sprite.__init__(self)

        self.COORDINATES = (x - 25, y - 25)
        self.DIRECTION = direction
        self.status = 1
        self.type = 'Enemy'  # Задаёт класс

        if speed == 0:
            self.SPEED = randint(5, 7)

        else:
            self.SPEED = speed


class Robber(Enemy):
    def __init__(self, x, y, direction: str = 'Right'):
        Enemy.__init__(self, x, y, direction)

        if self.DIRECTION == 'Right':
            self.image = right_robber_image

        else:
            self.image = left_robber_image

        self.image.set_colorkey('white')
        self.type = 'Robber'

        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def update(self):
        if pygame.sprite.collide_mask(self, player):
            faced(life)


class Bullet(Enemy):
    # При инициализации пули надо ОБЯЗАТЕЛЬНО указать местоположение пули и где она будет появляться
    # Также можно указать число кадров после которых пуля появиться
    # Направление пули, а также скорость, направление НЕ РАБОТАЕТ!
    def __init__(self, x, y, where_bullet, delay: int = 0, direction: str = 'Right', speed=0):
        Enemy.__init__(self, x, y, direction, speed)
        self.WHERE_BULLET = where_bullet
        self.delay = delay
        self.INITIAL_DELAY = delay

        if self.delay == 0:
            self.image = bullet_image
            self.image.set_colorkey('white')

        else:
            self.image = white_image
            self.image.set_colorkey('white')

        self.type = 'Bullet'

        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def update(self):
        if self.delay == 0:
            if self.image == white_image:
                self.image = bullet_image
                self.image.set_colorkey('white')

            if pygame.sprite.collide_mask(self, player):
                faced(life)

            elif self.DIRECTION == 'Right':
                if self.rect.x >= WIDTH:
                    self.rect.x = self.WHERE_BULLET[0]

                else:
                    self.rect.x += self.SPEED

            elif self.DIRECTION == 'Left':
                if self.rect.x <= 0:
                    self.rect.x = self.WHERE_BULLET[0]

                else:
                    self.rect.x -= self.SPEED

        else:
            self.delay -= 1


# Класс Перекати поел, наследуется от класса Враг
# Принимает координаты, направление и скорость движения
class Tumbleweed(Enemy):
    def __init__(self, x, y, direction: str = 'Right', speed: int = 0):
        Enemy.__init__(self, x, y, direction, speed)
        self.type = 'Tumbleweed'  # Задаёт класс

        self.image = tumbleweed_image
        self.image.set_colorkey('white')

        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def update(self):
        if pygame.sprite.collide_mask(self, player):
            faced(life)

        elif self.rect.x > WIDTH:
            self.rect.x = -50

        else:
            self.rect.x += self.SPEED


class Key(pygame.sprite.Sprite):
    # При создании объекта класса надо задать координаты, а также есть возможность выбрать уровень
    def __init__(self, x, y, status: int = 1):
        pygame.sprite.Sprite.__init__(self)
        self.hide = False  # Переменная отвечает за показывание картинки
        self.COORDINATES = (x - 25, y - 25)
        self.type = 'Key'  # Задаёт класс
        self.status = status

        if status == 1:
            self.image = key_image
            self.image.set_colorkey('white')

        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def update(self):
        if not self.hide:
            if self.image == white_image:
                if self.status == 1:
                    self.image = key_image
                    self.image.set_colorkey('white')

            if pygame.sprite.collide_mask(self, player):
                self.bring_key()

    def bring_key(self):
        self.hide = True

        self.image = white_image
        self.image.set_colorkey('white')


class Point(pygame.sprite.Sprite):  # Класс очков которые если взять то оно зачислется
    # При создании объекта класса надо задать координаты, сколько даёт денег,
    # Есть ли ключ (Если да, то указать ключ) и уровень
    def __init__(self, x, y, money: int = 100, have_key: Key = False, status: int = 1):
        pygame.sprite.Sprite.__init__(self)
        self.have_key = have_key
        self.hide = False  # Переменная отвечает за показывание картинки
        self.COORDINATES = (x - 25, y - 25)
        self.type = 'Point'  # Задаёт класс
        self.money: int = money
        self.status = status

        if self.have_key is not False:
            self.image = white_image
            self.image.set_colorkey('white')

        else:
            if status == 1:
                self.image = point_image
                self.image.set_colorkey('white')

            else:
                self.image = white_image
                self.image.set_colorkey('white')

        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def update(self):
        if self.have_key is not False:
            if self.have_key.hide:
                self.reaction()

            else:
                self.image = white_image
                self.image.set_colorkey('white')

        else:
            self.reaction()

    def reaction(self):
        if pygame.sprite.collide_mask(self, player):
            get_point(self, self.money)

        if self.hide:  # Если равен правде, то деньги не будут показываться
            self.image = white_image
            self.image.set_colorkey('white')

        else:
            self.image = point_image
            self.image.set_colorkey('white')


class Score:  # Класс счёта
    def __init__(self, shield, points: str = '000000',
                 color=(237, 28, 36)):  # При создании объекта класса надо задать счёт и цвет очков
        self.points = points  # Создаю переменную очки в которую надо записывать счёт
        self.screen = shield
        self.color = color
        self.font = pygame.font.Font(None, 45)
        self.type = 'Score'  # Задаёт класс
        self.status = 1

    def update(self, color=(237, 28, 36)):  # Этот метод позволит обновлять счёт
        text = self.font.render(self.points, True, color)  # Рисую счёт - коричневый цвет
        text_w = text.get_width()
        text_h = text.get_height()
        text_x = 15
        text_y = 15
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, color, (text_x - 5, text_y - 5,
                                         text_w + 10, text_h + 5), 1)


class Hedge(pygame.sprite.Sprite):
    # Класс переграда
    # При создании объекта класса надо указать координаты и статус
    # Статус - Картинка объекта
    def __init__(self, x, y, status: int = 1):
        pygame.sprite.Sprite.__init__(self)
        self.status = status
        self.COORDINATES = (x - 25, y - 25)
        self.type = 'Hedge'  # Задаёт класс

        if self.status == 1:
            self.image = cactus_image
            self.image.set_colorkey('white')

        else:
            self.image = thorny_bush_image
            self.image.set_colorkey('white')

        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def update(self):
        if pygame.sprite.collide_mask(self, player):
            faced(life)

    # Создаем игру и окно


# Класс Жизнь выводит сердце на экран и количество жизней
class Life(pygame.sprite.Sprite):
    # При инициализации надо указать координаты сердца, изображение сердца
    # Экран куда выводится текст и объект счёта, также можно указать цвет текста (красный по умолчанию)
    def __init__(self, x, y, heart, shield, account: Score, color=(237, 28, 36)):
        pygame.sprite.Sprite.__init__(self)

        self.COORDINATES = x - 25, y - 25
        self.image = heart

        self.image.set_colorkey("green")
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.status = 1
        self.type = 'Life'
        self.screen = shield
        self.color = color
        self.font = pygame.font.Font(None, 55)

        self.life = '5'
        self.score: Score = account

    def update(self, color=(237, 28, 36)):  # Этот метод позволит обновлять счёт
        text = self.font.render(self.life, True, color)  # Рисую счёт - коричневый цвет
        text_x = 675
        text_y = 10
        screen.blit(text, (text_x, text_y))


make_matrix()

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Adventure experience")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
sprites = []
coordinates = []  # В этой переменной содержаться координаты всех персонажей

player_image = load_image('bigger_player.png')
player_left_image = load_image('bigger_left_player.png')
player_right_image = load_image('bigger_right_player.png')
player_back_image = load_image('bigger_back_player.png')
player = Player()

heart_image = load_image('heart.png')
score = Score(screen)
life = Life(725, 25, heart_image, screen, score)

life_group.add(life)

tumbleweed_image = load_image('tumbleweed.png')
tumbleweed_left_image = load_image('tumbleweed_left.png')
tumbleweed_back_image = load_image('tumbleweed_back.png')
tumbleweed_right_image = load_image('tumbleweed_right.png')

bullet_image = load_image('bullet.png')

right_robber_image = load_image('right_robber.png')
left_robber_image = load_image('left_robber.png')

cactus_image = load_image('cactus.png')
thorny_bush_image = load_image('thorny_bush.png')

# Создаю восемь объектов класса перекати поел которые средние
first_tumbleweed = Tumbleweed(0, 375, 'Right', 6)
first_second_tumbleweed = Tumbleweed(650, 375, 'Right', 6)
first_third_tumbleweed = Tumbleweed(50, 375, 'Right', 6)
first_fourth_tumbleweed = Tumbleweed(200, 375, 'Right', 6)
first_fifth_tumbleweed = Tumbleweed(250, 375, 'Right', 6)
first_sixth_tumbleweed = Tumbleweed(400, 375, 'Right', 6)
first_seventh_tumbleweed = Tumbleweed(450, 375, 'Right', 6)
first_eighth_tumbleweed = Tumbleweed(600, 375, 'Right', 6)

# Создаю восемь объектов класса перекати поел которые самые верхние
second_tumbleweed = Tumbleweed(100, 325, 'Right', 7)
second_second_tumbleweed = Tumbleweed(750, 325, 'Right', 7)
second_third_tumbleweed = Tumbleweed(150, 325, 'Right', 7)
second_fourth_tumbleweed = Tumbleweed(300, 325, 'Right', 7)
second_fifth_tumbleweed = Tumbleweed(350, 325, 'Right', 7)
second_sixth_tumbleweed = Tumbleweed(500, 325, 'Right', 7)
second_seventh_tumbleweed = Tumbleweed(550, 325, 'Right', 7)
second_eighth_tumbleweed = Tumbleweed(700, 325, 'Right', 7)

# Создаю семь объектов класса перекати поел которые вторые нижние
third_first_tumbleweed = Tumbleweed(50, 475, 'Right', 9)
third_second_tumbleweed = Tumbleweed(100, 475, 'Right', 9)
third_third_tumbleweed = Tumbleweed(300, 475, 'Right', 9)
third_fourth_tumbleweed = Tumbleweed(350, 475, 'Right', 9)
third_fifth_tumbleweed = Tumbleweed(400, 475, 'Right', 9)
third_sixth_tumbleweed = Tumbleweed(600, 475, 'Right', 9)
third_seventh_tumbleweed = Tumbleweed(650, 475, 'Right', 9)

# Создаю четыре объекта класса перекати поел которые самые нижние
fourth_first_tumbleweed = Tumbleweed(25, 525, 'Right', 10)
fourth_second_tumbleweed = Tumbleweed(75, 525, 'Right', 10)
fourth_third_tumbleweed = Tumbleweed(275, 525, 'Right', 10)
fourth_fourth_tumbleweed = Tumbleweed(325, 525, 'Right', 10)
fourth_fifth_tumbleweed = Tumbleweed(525, 525, 'Right', 10)
fourth_sixth_tumbleweed = Tumbleweed(575, 525, 'Right', 10)

key_image = load_image('key.png')
key = Key(475, 25)

point_image = load_image('point.png')
white_image = load_image('white.png')  # Белое изображение нужно для очков
point = Point(75, 625, 1000)
high_point = Point(675, 175, 4000, key)

# Создаю пули
first_first_bullet = Bullet(50, 125, (50, 125), 0, 'Right', 9)
first_second_bullet = Bullet(50, 125, (50, 125), 36, 'Right', 9)

second_first_bullet = Bullet(50, 175, (50, 175), 18, 'Right', 9)
second_second_bullet = Bullet(50, 175, (50, 175), 54, 'Right', 9)

third_first_bullet = Bullet(50, 75, (50, 75), 58, 'Right', 9)
third_second_bullet = Bullet(50, 75, (50, 75), 94, 'Right', 9)

first_robber = Robber(25, 125, 'Right')
second_robber = Robber(25, 175, 'Right')
third_robber = Robber(25, 75, 'Right')

second_cactus = Hedge(25, 575, 1)
third_cactus = Hedge(25, 625, 1)
fourth_cactus = Hedge(75, 575, 1)
eighth_cactus = Hedge(175, 575, 1)
ninth_cactus = Hedge(175, 625, 1)
eleventh_cactus = Hedge(225, 575, 1)
twelfth_cactus = Hedge(225, 625, 1)

first_first_thorny_bush = Hedge(25, 25, 2)
first_second_thorny_bush = Hedge(225, 75, 2)
first_third_thorny_bush = Hedge(325, 25, 2)
first_fourth_thorny_bush = Hedge(525, 25, 2)
first_fifth_thorny_bush = Hedge(575, 25, 2)
first_sixth_thorny_bush = Hedge(625, 25, 2)
first_seventh_thorny_bush = Hedge(675, 25, 2)
first_eight_thorny_bush = Hedge(725, 25, 2)

second_first_thorny_bush = Hedge(75, 75, 2)
second_second_thorny_bush = Hedge(125, 75, 2)
second_third_thorny_bush = Hedge(425, 75, 2)
second_fourth_thorny_bush = Hedge(475, 75, 2)
second_fifth_thorny_bush = Hedge(525, 75, 2)
second_sixth_thorny_bush = Hedge(725, 75, 2)

third_first_thorny_bush = Hedge(75, 125, 2)
third_second_thorny_bush = Hedge(225, 25, 2)
third_third_thorny_bush = Hedge(225, 125, 2)
third_fourth_thorny_bush = Hedge(275, 125, 2)
third_fifth_thorny_bush = Hedge(325, 125, 2)
third_sixth_thorny_bush = Hedge(525, 125, 2)
third_seventh_thorny_bush = Hedge(625, 125, 2)
third_eight_thorny_bush = Hedge(725, 125, 2)

fourth_first_thorny_bush = Hedge(175, 175, 2)
fourth_third_thorny_bush = Hedge(625, 175, 2)
fourth_fourth_thorny_bush = Hedge(725, 175, 2)

fifth_first_thorny_bush = Hedge(25, 225, 2)
fifth_second_thorny_bush = Hedge(125, 225, 2)
fifth_third_thorny_bush = Hedge(175, 225, 2)
fifth_fourth_thorny_bush = Hedge(275, 225, 2)
fifth_fifth_thorny_bush = Hedge(325, 225, 2)
fifth_sixth_thorny_bush = Hedge(375, 225, 2)
fifth_seventh_thorny_bush = Hedge(425, 225, 2)
fifth_eighth_thorny_bush = Hedge(475, 225, 2)
fifth_ninth_thorny_bush = Hedge(525, 225, 2)
fifth_tenth_thorny_bush = Hedge(575, 225, 2)
fifth_eleventh_thorny_bush = Hedge(625, 225, 2)
fifth_twelfth_thorny_bush = Hedge(675, 225, 2)
fifth_thirteenth_thorny_bush = Hedge(725, 225, 2)

# Добавляю все спрайты

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

add_sprite(third_first_tumbleweed)
add_sprite(third_second_tumbleweed)
add_sprite(third_third_tumbleweed)
add_sprite(third_fourth_tumbleweed)
add_sprite(third_fifth_tumbleweed)
add_sprite(third_sixth_tumbleweed)
add_sprite(third_seventh_tumbleweed)

add_sprite(fourth_first_tumbleweed)
add_sprite(fourth_second_tumbleweed)
add_sprite(fourth_third_tumbleweed)
add_sprite(fourth_fourth_tumbleweed)
add_sprite(fourth_fifth_tumbleweed)
add_sprite(fourth_sixth_tumbleweed)

add_sprite(key)
add_sprite(point)
add_sprite(high_point)

add_sprite(first_first_bullet)
add_sprite(first_second_bullet)

add_sprite(second_first_bullet)
add_sprite(second_second_bullet)

add_sprite(third_first_bullet)
add_sprite(third_second_bullet)

add_sprite(first_robber)
add_sprite(second_robber)
add_sprite(third_robber)

add_sprite(second_cactus)
add_sprite(third_cactus)
add_sprite(fourth_cactus)
add_sprite(eighth_cactus)
add_sprite(ninth_cactus)
add_sprite(eleventh_cactus)
add_sprite(twelfth_cactus)

add_sprite(first_first_thorny_bush)
add_sprite(first_second_thorny_bush)
add_sprite(first_third_thorny_bush)
add_sprite(first_fourth_thorny_bush)
add_sprite(first_fifth_thorny_bush)
add_sprite(first_sixth_thorny_bush)
add_sprite(first_seventh_thorny_bush)
add_sprite(first_eight_thorny_bush)

add_sprite(second_first_thorny_bush)
add_sprite(second_second_thorny_bush)
add_sprite(second_third_thorny_bush)
add_sprite(second_fourth_thorny_bush)
add_sprite(second_fifth_thorny_bush)
add_sprite(second_sixth_thorny_bush)

add_sprite(third_first_thorny_bush)
add_sprite(third_second_thorny_bush)
add_sprite(third_third_thorny_bush)
add_sprite(third_fourth_thorny_bush)
add_sprite(third_fifth_thorny_bush)
add_sprite(third_sixth_thorny_bush)
add_sprite(third_seventh_thorny_bush)
add_sprite(third_eight_thorny_bush)

add_sprite(fourth_first_thorny_bush)
add_sprite(fourth_third_thorny_bush)
add_sprite(fourth_fourth_thorny_bush)

add_sprite(fifth_first_thorny_bush)
add_sprite(fifth_second_thorny_bush)
add_sprite(fifth_third_thorny_bush)
add_sprite(fifth_fourth_thorny_bush)
add_sprite(fifth_fifth_thorny_bush)
add_sprite(fifth_sixth_thorny_bush)
add_sprite(fifth_seventh_thorny_bush)
add_sprite(fifth_eighth_thorny_bush)
add_sprite(fifth_ninth_thorny_bush)
add_sprite(fifth_tenth_thorny_bush)
add_sprite(fifth_eleventh_thorny_bush)
add_sprite(fifth_twelfth_thorny_bush)
add_sprite(fifth_thirteenth_thorny_bush)

add_sprite(life)


# Функция цикла игры
def third_level(running: bool = True, points: str = '000000'):
    global faced_bool
    global win_bool
    global stop_bool

    global life
    global screen
    global score
    global state_points

    if points is not None:
        state_points = points
        score.points = points

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Цикл игры
    while running:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)

        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if not faced_bool and not win_bool and not stop_bool:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        player.go_into_bush('Up')

                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        player.go_into_bush('Down')

                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        player.go_into_bush('Right')

                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        player.go_into_bush('Left')

                    elif event.key == pygame.K_ESCAPE:
                        stop_bool = True

                else:
                    if event.key == pygame.K_SPACE:
                        if win_bool:
                            your_record: str = record()

                            return your_record

                        if faced_bool:
                            if life.life == '0':
                                life.life = '5'
                                return_back()
                                faced_bool = False

                            else:
                                life.life = str(int(life.life) - 1)
                                return_back()
                                faced_bool = False

                    elif stop_bool:
                        if event.key == pygame.K_ESCAPE:
                            stop_bool = False

            else:
                if win_bool:
                    win()

                elif faced_bool:
                    faced(life)

        # Обновление
        screen.fill((222, 184, 135))

        if not faced_bool and not win_bool and not stop_bool:
            all_sprites.update()

        # Рендеринг
        all_sprites.draw(screen)
        score.update()
        life_group.update()
        life_group.draw(screen)

        # Вывод клетчатого поля
        if faced_bool:
            faced(life)

        if win_bool:
            win()

        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()
