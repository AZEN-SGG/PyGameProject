import pygame
import os
import sys

WIDTH = 650
HEIGHT = 650
FPS = 20

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

game_folder = os.path.dirname(__file__)
data_folder = os.path.join(game_folder, 'data')


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


def terminate():
    pygame.quit()
    sys.exit()


class Shark(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, SPEED, status):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.SPEED = SPEED
        self.status = status

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
            if self.rect.y == HEIGHT:
                self.rect.y = -50
        if self.status == 3:
            self.rect.y -= self.SPEED
            if self.rect.y == -50:
                self.rect.y = HEIGHT


class Board:
    def render(self, screen, coor):
        j, i = coor
        j //= 50
        i //= 50
        for y in range(HEIGHT // 50):
            for x in range(WIDTH // 50):
                if not (abs(y - j) <= 1 and abs(x - i) <= 1):
                    pygame.draw.rect(screen, 'black',
                                     (x * 50, y * 50, 50, 50))


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


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Across The Road")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

board = Board()

player_image = pygame.image.load(os.path.join(data_folder, 'aqualunger.png')).convert()
player = Player()

all_sprites.add(player)
shark1 = Shark(load_image("data/" + "shark_up.png"), 4, 1, WIDTH - 50, HEIGHT - 100, 5, 3)
shark2 = Shark(load_image("data/" + "shark_down.png"), 4, 1, 0, 100, 5, 1)
shark3 = Shark(load_image("data/" + "shark_down.png"), 4, 1, 0, 300, 5, 1)
shark4 = Shark(load_image("data/" + "shark_up.png"), 4, 1, WIDTH - 50, 100, 5, 3)
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
            if event.key == pygame.K_w:
                player.go_up()

            elif event.key == pygame.K_s:
                player.go_down()

            elif event.key == pygame.K_d:
                player.go_right()

            elif event.key == pygame.K_a:
                player.go_left()

    screen.fill((0, 0, 139))
    # Обновление
    all_sprites.update()

    # Рендеринг
    all_sprites.draw(screen)
    # board.render(screen, player.get_rects())
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
