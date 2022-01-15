import pygame
import os

WIDTH = 750
HEIGHT = 650
FPS = 30
game_folder = os.path.dirname(__file__)
data_folder = os.path.join(game_folder, 'data')

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


pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Across The Road")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
board = Board()
player_image = pygame.image.load(os.path.join(data_folder, 'shlapa.png')).convert()
player = Player()



all_sprites.add(player)


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
    screen.fill((123, 34, 52))
    # Обновление
    all_sprites.update()
    board.render(screen)

    # Рендеринг
    all_sprites.draw(screen)
    # Вывод клетчатого поля
    board.render(screen)

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()
pygame.quit()
