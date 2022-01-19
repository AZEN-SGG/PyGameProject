import pygame
from os import path
from sys import exit
from random import choice

WIDTH = 750
HEIGHT = 650
FPS = 10

game_folder = path.dirname(__file__)
data_folder = path.join(game_folder, 'data')
boiler_coord = [[175, 25], [225, 125], [725, 225], [275, 525], [275, 225]]
poison_coord1 = [[25, 125], [175, 225], [725, 625]]
poison_coord2 = [[325, 25], [425, 175], [275, 625]]
poison_coord3 = [[725, 525], [325, 325], [625, 475]]
poison_coord4 = [[175, 525], [25, 325], [75, 525]]
key_coord = [[675, 125], [125, 125], [125, 525], [575, 475]]

matrix = [['' for _ in range(15)] for i in range(13)]
BOILER = False
KEY = False

stop_bool: bool = False
win_bool: bool = False
faced_bool: bool = False

state_points: str = '000000'


# Функция выключает программу
def terminate():
    # Выключает pygame
    pygame.quit()
    # Выключает всю программу
    exit()


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


def win():  # функция победы
    global win_bool  # переменная отвечающая за работоспособность спрайтов
    win_bool = True  # При win_bool равном правде все спрайты останавливаются

    font = pygame.font.Font(None, 50)
    text = font.render("Вы выиграли", True, 'white')
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (255, 4, 86), (text_x - 10, text_y - 10,
                                            text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


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


def return_back():  # Возвращение спрайтов на исходные позиции
    life.take_away_life()
    bat1.reloaded()
    bat2.reloaded()
    bat3.reloaded()
    bat4.reloaded()
    bat5.reloaded()
    bat6.reloaded()
    bat7.reloaded()
    bat8.reloaded()
    player.reloaded()
    key.reloaded()
    boiler.reloaded()

    if life.give_life() < 0:  # Обнуление очков при нехватке жизней
        score.discharge()
        life.alive()
        potion1.status_collected()
        potion2.status_collected()
        potion3.status_collected()
        poison1.status_collected()
        poison2.status_collected()
        poison3.status_collected()
        poison4.status_collected()

    potion1.reloaded()
    potion2.reloaded()
    potion3.reloaded()
    poison1.reloaded()
    poison2.reloaded()
    poison3.reloaded()
    poison4.reloaded()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image
        self.image.set_colorkey('white')

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 25)

    def get_rects(self):
        return self.rect.y, self.rect.x

    def go_up(self):
        self.image = player_image
        self.image.set_colorkey('white')
        if self.rect.y == 0:
            pass

        else:
            y = (self.rect.y - 50) // 50
            if matrix[y][self.rect.x // 50] == 'HideFlame':
                flame48.update()
                flame49.update()
                flame50.update()
                flame51.update()
                flame52.update()
                flame53.update()
                flame54.update()
                flame55.update()
                flame56.update()
                flame57.update()
                flame58.update()
                flame59.update()
                flame60.update()
                flame61.update()
                flame62.update()
                self.rect.y -= 50

            elif matrix[y][self.rect.x // 50] != 'Flame':
                self.rect.y -= 50

    def go_down(self):
        self.image = player_down_image
        self.image.set_colorkey('white')
        if self.rect.y == HEIGHT - 50:
            pass

        else:
            y = (self.rect.y + 50) // 50
            if matrix[y][self.rect.x // 50] == 'HideFlame':
                flame48.update()
                flame49.update()
                flame50.update()
                flame51.update()
                flame52.update()
                flame53.update()
                flame54.update()
                flame55.update()
                flame56.update()
                flame57.update()
                flame58.update()
                flame59.update()
                flame60.update()
                flame61.update()
                flame62.update()
                self.rect.y += 50

            elif matrix[y][self.rect.x // 50] != 'Flame':
                self.rect.y += 50

    def go_right(self):
        self.image = player_right_image
        self.image.set_colorkey('white')
        if self.rect.x == WIDTH - 50:
            if matrix[self.rect.y // 50][0] != 'Flame':
                self.rect.x = 0

        else:
            x = (self.rect.x + 50) // 50
            if matrix[self.rect.y // 50][x] == 'HideFlame':
                flame48.update()
                flame49.update()
                flame50.update()
                flame51.update()
                flame52.update()
                flame53.update()
                flame54.update()
                flame55.update()
                flame56.update()
                flame57.update()
                flame58.update()
                flame59.update()
                flame60.update()
                flame61.update()
                flame62.update()
                self.rect.x += 50

            elif matrix[self.rect.y // 50][x] != 'Flame':
                self.rect.x += 50

    def go_left(self):
        self.image = player_left_image
        self.image.set_colorkey('white')
        if self.rect.x == 0:
            self.rect.x = WIDTH - 50

        else:
            x = (self.rect.x - 50) // 50
            if matrix[self.rect.y // 50][x] == 'HideFlame':
                flame48.update()
                flame49.update()
                flame50.update()
                flame51.update()
                flame52.update()
                flame53.update()
                flame54.update()
                flame55.update()
                flame56.update()
                flame57.update()
                flame58.update()
                flame59.update()
                flame60.update()
                flame61.update()
                flame62.update()
                self.rect.x -= 50

            elif matrix[self.rect.y // 50][x] != 'Flame':
                self.rect.x -= 50

    def reloaded(self):
        self.image = player_image
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH / 2, HEIGHT - 25


class Flame(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        matrix[y // 50][x // 50] = 'Flame'
        self.frames = []
        self.cur_frame = 0
        self.cut_sheet(sheet, columns, rows)
        self.image = self.frames[self.cur_frame]
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def cut_sheet(self, sheet, columns, rows):  # получение изображения
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
        self.image.set_colorkey('white')


class Hide_Flame(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        matrix[y // 50][x // 50] = 'HideFlame'
        self.frames = []
        self.cur_frame = 0
        self.cut_sheet(sheet, columns, rows)
        self.image = self.frames[self.cur_frame]
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.hide = False

    def cut_sheet(self, sheet, columns, rows):  # получение изображения
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
        self.image.set_colorkey('white')
        if player.rect.center[0] == self.rect.centerx - 50 and player.rect.center[1] == self.rect.centery:
            self.hide = True
            self.image = white_image
            self.image.set_colorkey('white')

        elif player.rect.center[0] == self.rect.centerx + 50 and player.rect.center[1] == self.rect.centery:
            self.hide = True
            self.image = white_image
            self.image.set_colorkey('white')

        elif player.rect.center[1] == self.rect.centery + 50 and player.rect.center[0] == self.rect.centerx:
            self.hide = True
            self.image = white_image
            self.image.set_colorkey('white')

        elif player.rect.center[1] == self.rect.centery - 50 and player.rect.center[0] == self.rect.centerx:
            self.hide = True
            self.image = white_image
            self.image.set_colorkey('white')

        elif player.rect.center == self.rect.center:
            self.hide = True
            self.image = white_image
            self.image.set_colorkey('white')

        else:
            self.hide = False
            self.image = self.frames[self.cur_frame]
            self.image.set_colorkey('white')


class Potion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = potion_image
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.hide = False
        self.collected = False

    def update(self):
        if not self.hide:
            if self.image == white_image:
                self.image = potion_image
                self.image.set_colorkey('white')

            if pygame.sprite.collide_mask(self, player):
                self.adding_points()
                self.collected = True

    def adding_points(self):  # добавление очков
        self.hide = True
        self.collected = True

        self.image = white_image
        self.image.set_colorkey('white')
        score.add_points(1000)

    def reloaded(self):
        if not self.collected:
            self.hide = False

    def status_collected(self):
        self.collected = False


class Boiler(pygame.sprite.Sprite):
    # При создании объекта класса надо задать координаты, а также есть возможность выбрать уровень
    def __init__(self, coord):
        x, y = coord[0], coord[1]
        pygame.sprite.Sprite.__init__(self)  # Переменная отвечает за показывание картинки
        self.image = boiler_image
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def update(self):
        if pygame.sprite.collide_mask(self, player):
            self.bring_boiler()

    def bring_boiler(self):
        global BOILER
        BOILER = True

        self.rect.x = 575
        self.rect.y = 0
        poison1.change_hide()
        poison2.change_hide()
        poison3.change_hide()
        poison4.change_hide()

    def reloaded(self):
        global boiler_coord
        self.__init__(choice(boiler_coord))


class Poison(pygame.sprite.Sprite):
    def __init__(self, coord):
        x, y = coord[0], coord[1]
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
                self.image = poison_image
                self.image.set_colorkey('white')

            if pygame.sprite.collide_mask(self, player):
                self.adding_points()

    def adding_points(self):  # добавление очков
        self.hide = True
        self.collected = True

        self.image = white_image
        self.image.set_colorkey('white')
        score.add_points(500)

    def change_hide(self):
        if not self.collected:
            self.hide = False
            self.image = poison_image
            self.image.set_colorkey('white')

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
        self.status = 1

    # Функция получает количество очков полученных при собирании звёздочки
    # Если очков выходит больше тысячи прибавляет жизнь
    def add_points(self, point):
        global life

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
        self.points = state_points


class Life(pygame.sprite.Sprite):
    def __init__(self, screen, color=(237, 28, 36)):
        pygame.sprite.Sprite.__init__(self)

        self.COORDINATS = 675, 25
        self.image = heart_image
        self.image.set_colorkey("green")
        self.rect = self.image.get_rect()
        self.rect.center = 725, 25

        self.screen = screen
        self.color = color
        self.font = pygame.font.Font(None, 55)

        self.life = '5'

    def update(self, color=(237, 28, 36)):  # Этот метод позволит обновлять счёт
        text = self.font.render(self.life, True, color)  # Рисую счёт - коричневый цвет
        text_x = 675
        text_y = 10
        screen.blit(text, (text_x, text_y))

    def take_away_life(self):
        self.life = str(int(self.life) - 1)

    def give_life(self):
        return int(self.life)

    def alive(self):
        self.life = '5'


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = closing_door_image
        self.image.set_colorkey('green')
        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def update(self):
        global win_bool

        if KEY:
            self.image = opening_door_image
            self.image.set_colorkey('green')
            if pygame.sprite.collide_mask(self, player):
                win_bool = True

        else:
            self.image = closing_door_image
            self.image.set_colorkey('green')


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
        self.rect.x = 625
        self.rect.y = 0

    def reloaded(self):
        global key_coord
        self.__init__(choice(key_coord))


class Bat(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, SPEED, status, spi=[]):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image.set_colorkey('white')
        self.rect = self.rect.move(x, y)
        self.SPEED = SPEED
        self.status = status
        if spi == []:
            self.spi = [sheet, columns, rows, x, y, SPEED, status]

        else:
            self.spi = spi

    def cut_sheet(self, sheet, columns, rows):  # получение изображения
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        global bat_image
        global bat_right_image

        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.image.set_colorkey('white')
        if self.status == 1:
            self.rect.x -= self.SPEED
            if self.rect.x <= -20:
                self.__init__(bat_right_image, 3, 1, 0, 510, 20, 2, self.spi)

        elif self.status == 2:
            self.rect.x += self.SPEED
            if self.rect.x >= 710:
                self.__init__(bat_image, 3, 1, 710, 510, 20, 1, self.spi)

        elif self.status == 3:
            self.rect.x -= self.SPEED
            if self.rect.x <= -20:
                self.__init__(bat_right_image, 3, 1, 0, 105, 20, 4, self.spi)

        elif self.status == 4:
            self.rect.x += self.SPEED
            if self.rect.x >= 710:
                self.__init__(bat_image, 3, 1, WIDTH - 50, 105, 20, 3, self.spi)

        elif self.status == 5:
            self.rect.y += self.SPEED
            if self.rect.y >= 460:
                self.__init__(bat_right_image, 3, 1, 105, 460, 20, 6, self.spi)

        elif self.status == 6:
            self.rect.x += self.SPEED
            if self.rect.x >= 590:
                self.__init__(bat_image, 3, 1, 590, 460, 20, 7, self.spi)

        elif self.status == 7:
            self.rect.y -= self.SPEED
            if self.rect.y <= 155:
                self.__init__(bat_image, 3, 1, 590, 155, 20, 8, self.spi)

        elif self.status == 8:
            self.rect.x -= self.SPEED
            if self.rect.x <= 105:
                self.__init__(bat_right_image, 3, 1, 105, 155, 20, 5, self.spi)

        elif self.status == 9:
            self.rect.x += self.SPEED
            if self.rect.x >= 545:
                self.__init__(bat_right_image, 3, 1, 545, 205, 20, 10, self.spi)

        elif self.status == 10:
            self.rect.y += self.SPEED
            if self.rect.y >= 405:
                self.__init__(bat_image, 3, 1, 545, 405, 20, 11, self.spi)

        elif self.status == 11:
            self.rect.x -= self.SPEED
            if self.rect.x <= 150:
                self.__init__(bat_right_image, 3, 1, 150, 405, 20, 12, self.spi)

        elif self.status == 12:
            self.rect.y -= self.SPEED
            if self.rect.y <= 205:
                self.__init__(bat_right_image, 3, 1, 150, 205, 20, 9, self.spi)

        if pygame.sprite.collide_mask(self, player):
            faced()

    def reloaded(self):  # возвращение на исходную позицию
        self.__init__(*self.spi)


pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Adventure experience")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
dop_sprites = pygame.sprite.Group()
score = Score(screen)

player_image = load_image('data/shlapa.png')
player_down_image = load_image('data/shlapa_down.png')
player_right_image = load_image('data/shlapa_right.png')
player_left_image = load_image('data/shlapa_left.png')
player = Player()

flame_image = load_image("data/flame.png")

flame1 = Flame(flame_image, 4, 1, 25, 75)
flame2 = Flame(flame_image, 4, 1, 175, 75)
flame3 = Flame(flame_image, 4, 1, 225, 75)
flame4 = Flame(flame_image, 4, 1, 275, 75)
flame5 = Flame(flame_image, 4, 1, 325, 75)
flame6 = Flame(flame_image, 4, 1, 425, 75)
flame7 = Flame(flame_image, 4, 1, 475, 75)
flame8 = Flame(flame_image, 4, 1, 525, 75)
flame9 = Flame(flame_image, 4, 1, 575, 75)
flame10 = Flame(flame_image, 4, 1, 725, 75)

flame11 = Flame(flame_image, 4, 1, 125, 575)
flame12 = Flame(flame_image, 4, 1, 175, 575)
flame13 = Flame(flame_image, 4, 1, 225, 575)
flame14 = Flame(flame_image, 4, 1, 275, 575)
flame15 = Flame(flame_image, 4, 1, 325, 575)
flame16 = Flame(flame_image, 4, 1, 375, 575)
flame17 = Flame(flame_image, 4, 1, 425, 575)
flame18 = Flame(flame_image, 4, 1, 475, 575)
flame19 = Flame(flame_image, 4, 1, 525, 575)
flame20 = Flame(flame_image, 4, 1, 575, 575)
flame21 = Flame(flame_image, 4, 1, 625, 575)

flame22 = Flame(flame_image, 4, 1, 25, 175)
flame23 = Flame(flame_image, 4, 1, 75, 175)
flame24 = Flame(flame_image, 4, 1, 75, 225)
flame25 = Flame(flame_image, 4, 1, 75, 275)
flame26 = Flame(flame_image, 4, 1, 75, 375)
flame27 = Flame(flame_image, 4, 1, 75, 425)
flame28 = Flame(flame_image, 4, 1, 75, 475)

flame29 = Flame(flame_image, 4, 1, 25, 475)
flame30 = Flame(flame_image, 4, 1, 725, 175)
flame31 = Flame(flame_image, 4, 1, 675, 175)
flame32 = Flame(flame_image, 4, 1, 675, 225)
flame33 = Flame(flame_image, 4, 1, 675, 275)
flame34 = Flame(flame_image, 4, 1, 675, 375)
flame35 = Flame(flame_image, 4, 1, 675, 425)
flame36 = Flame(flame_image, 4, 1, 675, 475)
flame37 = Flame(flame_image, 4, 1, 725, 475)

flame38 = Flame(flame_image, 4, 1, 225, 275)
flame39 = Flame(flame_image, 4, 1, 275, 275)
flame40 = Flame(flame_image, 4, 1, 325, 275)
flame41 = Flame(flame_image, 4, 1, 375, 275)
flame42 = Flame(flame_image, 4, 1, 525, 275)
flame43 = Flame(flame_image, 4, 1, 525, 375)
flame44 = Flame(flame_image, 4, 1, 475, 375)
flame45 = Flame(flame_image, 4, 1, 425, 375)
flame46 = Flame(flame_image, 4, 1, 375, 375)
flame47 = Flame(flame_image, 4, 1, 225, 375)

flame48 = Hide_Flame(flame_image, 4, 1, 75, 75)
flame49 = Hide_Flame(flame_image, 4, 1, 125, 75)
flame50 = Hide_Flame(flame_image, 4, 1, 375, 75)
flame51 = Hide_Flame(flame_image, 4, 1, 625, 75)
flame52 = Hide_Flame(flame_image, 4, 1, 675, 75)
flame53 = Hide_Flame(flame_image, 4, 1, 175, 625)
flame54 = Hide_Flame(flame_image, 4, 1, 575, 625)
flame55 = Hide_Flame(flame_image, 4, 1, 75, 325)
flame56 = Hide_Flame(flame_image, 4, 1, 675, 325)
flame57 = Hide_Flame(flame_image, 4, 1, 425, 275)
flame58 = Hide_Flame(flame_image, 4, 1, 475, 275)
flame59 = Hide_Flame(flame_image, 4, 1, 525, 325)
flame60 = Hide_Flame(flame_image, 4, 1, 325, 375)
flame61 = Hide_Flame(flame_image, 4, 1, 275, 375)
flame62 = Hide_Flame(flame_image, 4, 1, 225, 325)

white_image = load_image('data/white.png')

potion_image = load_image('data/zelye.png')
potion1 = Potion(25, 425)
potion2 = Potion(725, 125)
potion3 = Potion(425, 325)

dop_sprites.add(potion1)
dop_sprites.add(potion2)
dop_sprites.add(potion3)

heart_image = load_image('data/heart.png')
life = Life(screen, score)

key_image = load_image('data/key.png')
key = Key(choice(key_coord))

dop_sprites.add(key)

boiler_image = load_image('data/boiler.png')
boiler = Boiler(choice(boiler_coord))

dop_sprites.add(boiler)

poison_image = load_image('data/dopzelye.png')
poison1 = Poison(choice(poison_coord1))
poison2 = Poison(choice(poison_coord2))
poison3 = Poison(choice(poison_coord3))
poison4 = Poison(choice(poison_coord4))

dop_sprites.add(poison1)
dop_sprites.add(poison2)
dop_sprites.add(poison3)
dop_sprites.add(poison4)

opening_door_image = load_image('data/opening_door.png')
closing_door_image = load_image('data/closing_door.png')
door = Door(375, 325)

# Создаю изображения летучих мышей
bat_image = load_image("data/bat.png")
bat_right_image = load_image("data/bat_right.png")

bat1 = Bat(bat_image, 3, 1, WIDTH - 50, 510, 15, 1, [])
bat2 = Bat(bat_right_image, 3, 1, 0, 510, 10, 2, [])
bat3 = Bat(bat_image, 3, 1, 350, 510, 10, 1, [])
bat4 = Bat(bat_right_image, 3, 1, 350, 510, 15, 2, [])

bat5 = Bat(bat_image, 3, 1, WIDTH - 50, 105, 15, 3, [])
bat6 = Bat(bat_right_image, 3, 1, 0, 105, 10, 4, [])
bat7 = Bat(bat_image, 3, 1, 350, 105, 10, 3, [])
bat8 = Bat(bat_right_image, 3, 1, 350, 105, 15, 4, [])

bat9 = Bat(bat_right_image, 3, 1, 105, 155, 15, 5, [])
bat10 = Bat(bat_right_image, 3, 1, 105, 460, 15, 6, [])
bat11 = Bat(bat_image, 3, 1, 590, 460, 15, 7, [])
bat12 = Bat(bat_image, 3, 1, 590, 155, 15, 8, [])

bat13 = Bat(bat_image, 3, 1, 350, 205, 15, 9, [])
bat14 = Bat(bat_image, 3, 1, 545, 310, 15, 10, [])
bat15 = Bat(bat_image, 3, 1, 350, 405, 15, 11, [])
bat16 = Bat(bat_right_image, 3, 1, 150, 310, 15, 12, [])

all_sprites.add(door)
all_sprites.add(key)
all_sprites.add(player)
all_sprites.add(flame1)
all_sprites.add(flame2)
all_sprites.add(flame3)
all_sprites.add(flame4)
all_sprites.add(flame5)
all_sprites.add(flame6)
all_sprites.add(flame7)
all_sprites.add(flame8)
all_sprites.add(flame9)
all_sprites.add(flame10)
all_sprites.add(flame11)
all_sprites.add(flame12)
all_sprites.add(flame13)
all_sprites.add(flame14)
all_sprites.add(flame15)
all_sprites.add(flame16)
all_sprites.add(flame17)
all_sprites.add(flame18)
all_sprites.add(flame19)
all_sprites.add(flame20)
all_sprites.add(flame21)
all_sprites.add(flame22)
all_sprites.add(flame23)
all_sprites.add(flame24)
all_sprites.add(flame25)
all_sprites.add(flame26)
all_sprites.add(flame27)
all_sprites.add(flame28)
all_sprites.add(flame29)
all_sprites.add(flame30)
all_sprites.add(flame31)
all_sprites.add(flame32)
all_sprites.add(flame33)
all_sprites.add(flame34)
all_sprites.add(flame35)
all_sprites.add(flame36)
all_sprites.add(flame37)
all_sprites.add(flame38)
all_sprites.add(flame39)
all_sprites.add(flame40)
all_sprites.add(flame41)
all_sprites.add(flame42)
all_sprites.add(flame43)
all_sprites.add(flame44)
all_sprites.add(flame45)
all_sprites.add(flame46)
all_sprites.add(flame47)
all_sprites.add(flame48)
all_sprites.add(flame49)
all_sprites.add(flame50)
all_sprites.add(flame51)
all_sprites.add(flame52)
all_sprites.add(flame53)
all_sprites.add(flame54)
all_sprites.add(flame55)
all_sprites.add(flame56)
all_sprites.add(flame57)
all_sprites.add(flame58)
all_sprites.add(flame59)
all_sprites.add(flame60)
all_sprites.add(flame61)
all_sprites.add(flame62)
all_sprites.add(potion1)
all_sprites.add(potion2)
all_sprites.add(potion3)
all_sprites.add(boiler)
all_sprites.add(poison1)
all_sprites.add(poison2)
all_sprites.add(poison3)
all_sprites.add(poison4)
all_sprites.add(life)

all_sprites.add(bat1)
all_sprites.add(bat2)
all_sprites.add(bat3)
all_sprites.add(bat4)
all_sprites.add(bat5)
all_sprites.add(bat6)
all_sprites.add(bat7)
all_sprites.add(bat8)
all_sprites.add(bat9)
all_sprites.add(bat10)
all_sprites.add(bat11)
all_sprites.add(bat12)
all_sprites.add(bat13)
all_sprites.add(bat14)
all_sprites.add(bat15)
all_sprites.add(bat16)


# Цикл игры all_sprites.add(flame1)
def second_level(running: bool = True, points: str = '000000'):
    global stop_bool
    global win_bool
    global faced_bool

    global all_sprites
    global score
    global state_points

    global KEY
    global BOILER

    # Если предыдущий уровень вернул в игру очки, то они добавляются сюда
    if points is not None:
        state_points = points
        score.points = points

    while running:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if not win_bool and not stop_bool and not faced_bool:
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
                        BOILER = False
                        KEY = False

                elif stop_bool:
                    if event.key == pygame.K_ESCAPE:
                        stop_bool = False

        screen.fill((123, 34, 52))

        if not faced_bool and not win_bool and not stop_bool:
            all_sprites.update()

        all_sprites.draw(screen)
        score.update()
        dop_sprites.update()

        if faced_bool:
            faced()

        if win_bool:
            win()

        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()
