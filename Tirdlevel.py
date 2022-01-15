import pygame
import os

WIDTH = 750
HEIGHT = 650
FPS = 10
game_folder = os.path.dirname(__file__)
data_folder = os.path.join(game_folder, 'data')

matrix = [['' for _ in range(15)] for i in range(13)]


def load_image(name, color_key=None):  # Функция для получения фотографий
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
        self.image.set_colorkey('white')
        self.image.set_colorkey('white')

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 25)
        print(self.rect.y)
        print(self.rect.x)

    def update(self):
        pass

    def go_up(self):
        self.image = player_image
        self.image.set_colorkey('white')
        if self.rect.y == 0:
            pass
        else:
            y = (self.rect.y - 50) // 50
            if matrix[y][self.rect.x // 50] != 'Flame':
                self.rect.y -= 50

    def go_down(self):
        self.image = player_down_image
        self.image.set_colorkey('white')
        if self.rect.y == HEIGHT - 50:
            pass
        else:
            y = (self.rect.y + 50) // 50
            if matrix[y][self.rect.x // 50] != 'Flame':
                self.rect.y += 50

    def go_right(self):
        self.image = player_right_image
        self.image.set_colorkey('white')
        if self.rect.x == WIDTH - 50:
            if matrix[self.rect.y // 50][0] != 'Flame':
                self.rect.x = 0

        else:
            x = (self.rect.x + 50) // 50
            if matrix[self.rect.y // 50][x] != 'Flame':
                self.rect.x += 50

    def go_left(self):
        self.image = player_left_image
        self.image.set_colorkey('white')
        if self.rect.x == 0:
            self.rect.x = WIDTH - 50

        else:
            x = (self.rect.x - 50) // 50
            if matrix[self.rect.y // 50][x] != 'Flame':
                self.rect.x -= 50


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
        matrix[y // 50][x // 50] = 'Flame'
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


pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Across The Road")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
board = Board()

player_image = pygame.image.load(os.path.join(data_folder, 'shlapa.png')).convert()
player_down_image = pygame.image.load(os.path.join(data_folder, 'shlapa_down.png')).convert()
player_right_image = pygame.image.load(os.path.join(data_folder, 'shlapa_right.png')).convert()
player_left_image = pygame.image.load(os.path.join(data_folder, 'shlapa_left.png')).convert()
player = Player()

flame1 = Flame(load_image("data/" + "flame.png"), 4, 1, 25, 75)
flame2 = Flame(load_image("data/" + "flame.png"), 4, 1, 175, 75)
flame3 = Flame(load_image("data/" + "flame.png"), 4, 1, 225, 75)
flame4 = Flame(load_image("data/" + "flame.png"), 4, 1, 275, 75)
flame5 = Flame(load_image("data/" + "flame.png"), 4, 1, 325, 75)
flame6 = Flame(load_image("data/" + "flame.png"), 4, 1, 425, 75)
flame7 = Flame(load_image("data/" + "flame.png"), 4, 1, 475, 75)
flame8 = Flame(load_image("data/" + "flame.png"), 4, 1, 525, 75)
flame9 = Flame(load_image("data/" + "flame.png"), 4, 1, 575, 75)
flame10 = Flame(load_image("data/" + "flame.png"), 4, 1, 725, 75)

flame11 = Flame(load_image("data/" + "flame.png"), 4, 1, 125, 575)
flame12 = Flame(load_image("data/" + "flame.png"), 4, 1, 175, 575)
flame13 = Flame(load_image("data/" + "flame.png"), 4, 1, 225, 575)
flame14 = Flame(load_image("data/" + "flame.png"), 4, 1, 275, 575)
flame15 = Flame(load_image("data/" + "flame.png"), 4, 1, 325, 575)
flame16 = Flame(load_image("data/" + "flame.png"), 4, 1, 375, 575)
flame17 = Flame(load_image("data/" + "flame.png"), 4, 1, 425, 575)
flame18 = Flame(load_image("data/" + "flame.png"), 4, 1, 475, 575)
flame19 = Flame(load_image("data/" + "flame.png"), 4, 1, 525, 575)
flame20 = Flame(load_image("data/" + "flame.png"), 4, 1, 575, 575)
flame21 = Flame(load_image("data/" + "flame.png"), 4, 1, 625, 575)

flame22 = Flame(load_image("data/" + "flame.png"), 4, 1, 25, 175)
flame23 = Flame(load_image("data/" + "flame.png"), 4, 1, 75, 175)
flame24 = Flame(load_image("data/" + "flame.png"), 4, 1, 75, 225)
flame25 = Flame(load_image("data/" + "flame.png"), 4, 1, 75, 275)
flame26 = Flame(load_image("data/" + "flame.png"), 4, 1, 75, 375)
flame27 = Flame(load_image("data/" + "flame.png"), 4, 1, 75, 425)
flame28 = Flame(load_image("data/" + "flame.png"), 4, 1, 75, 475)

flame29 = Flame(load_image("data/" + "flame.png"), 4, 1, 25, 475)
flame30 = Flame(load_image("data/" + "flame.png"), 4, 1, 725, 175)
flame31 = Flame(load_image("data/" + "flame.png"), 4, 1, 675, 175)
flame32 = Flame(load_image("data/" + "flame.png"), 4, 1, 675, 225)
flame33 = Flame(load_image("data/" + "flame.png"), 4, 1, 675, 275)
flame34 = Flame(load_image("data/" + "flame.png"), 4, 1, 675, 375)
flame35 = Flame(load_image("data/" + "flame.png"), 4, 1, 675, 425)
flame36 = Flame(load_image("data/" + "flame.png"), 4, 1, 675, 475)
flame37 = Flame(load_image("data/" + "flame.png"), 4, 1, 725, 475)

flame38 = Flame(load_image("data/" + "flame.png"), 4, 1, 225, 275)
flame39 = Flame(load_image("data/" + "flame.png"), 4, 1, 275, 275)
flame40 = Flame(load_image("data/" + "flame.png"), 4, 1, 325, 275)
flame41 = Flame(load_image("data/" + "flame.png"), 4, 1, 375, 275)
flame42 = Flame(load_image("data/" + "flame.png"), 4, 1, 525, 275)
flame43 = Flame(load_image("data/" + "flame.png"), 4, 1, 525, 375)
flame44 = Flame(load_image("data/" + "flame.png"), 4, 1, 475, 375)
flame45 = Flame(load_image("data/" + "flame.png"), 4, 1, 425, 375)
flame46 = Flame(load_image("data/" + "flame.png"), 4, 1, 375, 375)
flame47 = Flame(load_image("data/" + "flame.png"), 4, 1, 225, 375)

flame48 = Hide_Flame(load_image("data/" + "flame.png"), 4, 1, 75, 75)
flame49 = Hide_Flame(load_image("data/" + "flame.png"), 4, 1, 125, 75)
flame50 = Hide_Flame(load_image("data/" + "flame.png"), 4, 1, 375, 75)
flame51 = Hide_Flame(load_image("data/" + "flame.png"), 4, 1, 625, 75)
flame52 = Hide_Flame(load_image("data/" + "flame.png"), 4, 1, 675, 75)
flame53 = Hide_Flame(load_image("data/" + "flame.png"), 4, 1, 175, 625)
flame54 = Hide_Flame(load_image("data/" + "flame.png"), 4, 1, 575, 625)
flame55 = Hide_Flame(load_image("data/" + "flame.png"), 4, 1, 75, 325)
flame56 = Hide_Flame(load_image("data/" + "flame.png"), 4, 1, 675, 325)
flame57 = Hide_Flame(load_image("data/" + "flame.png"), 4, 1, 425, 275)
flame58 = Hide_Flame(load_image("data/" + "flame.png"), 4, 1, 475, 275)
flame59 = Hide_Flame(load_image("data/" + "flame.png"), 4, 1, 525, 325)
flame60 = Hide_Flame(load_image("data/" + "flame.png"), 4, 1, 325, 375)
flame61 = Hide_Flame(load_image("data/" + "flame.png"), 4, 1, 275, 375)
flame62 = Hide_Flame(load_image("data/" + "flame.png"), 4, 1, 225, 325)

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


# Цикл игрыall_sprites.add(flame1)
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
            if event.key == pygame.K_w:
                player.go_up()
            elif event.key == pygame.K_s:
                player.go_down()
            elif event.key == pygame.K_d:
                player.go_right()
            elif event.key == pygame.K_a:
                player.go_left()
    screen.fill((123, 34, 52))
    # Обновление
    all_sprites.update()

    # Рендеринг
    all_sprites.draw(screen)
    # Вывод клетчатого поля

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()
pygame.quit()
