import ThirdLevel
import FirstLevel
import SecondLevel

import pygame
from sys import exit
from os import path

WIDTH: int = 750
HEIGHT: int = 650
FPS: int = 20


# Функция загрузки изображения
def load_image(name, color_key=None):
    name = "data/" + name
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


# Функция выключает программу
def terminate():
    # Выключает pygame
    pygame.quit()
    # Выключает всю программу
    exit()


# Функция выводит правила игры
# Нужно задать имя файла изображения, а также можно указать цвет текста
def start_screen(text, fon_name: str, color: str = 'yellow', number: int = 30):
    # Создаём фон
    fon = pygame.transform.scale(load_image(fon_name), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, number)
    text_coord = 50

    for line in text:
        string_rendered = font.render(line, True, pygame.Color(color))
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


intro_text = ['                             Первый Уровень - Подводный Мир', '', '', '',
              "                                          ПРАВИЛА УРОВНЯ",
              "             Управление игроком -> кнопки WASD или стрелочки",
              '   Чтобы пройти уровень необходимо найти ключ и открыть им дверь', '',
              '                                       Два типа вознаграждения:',
              '                 1 - Обычные морские звёзды, 500 очков',
              '                 2 - Дорогие морские звёзды, нужен ключ, 1000 очков', '',
              '                                             Два типа врагов:',
              "     1 - Акулы, на них лучше не попадаться иначе умрёшь",
              '     2 - Кораллы, обычные препятствия, которые мешают пройти', '',
              '  Ваша задача - пройти уровень, собрав наибольшее количество очков']

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Adventure experience")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Отображаю правила первого уровня
start_screen(intro_text, 'FirstLevelFon.png')
score = FirstLevel.first_level(True)

intro_text = ['                             Второй Уровень - Путешествие в Ад', '', '', '',
              "                                          ПРАВИЛА УРОВНЯ",
              "             Управление игроком -> кнопки WASD или стрелочки",
              '   Чтобы пройти уровень необходимо найти ключ и открыть им дверь', '',
              '                                       Два типа вознаграждения:',
              '                 1 - Зелёные зелья, нужен котел, 500 очков',
              '                 2 - Красные зелья, 1000 очков', '',
              '                                             Два типа врагов:',
              "     1 - Летучие Мыши, на них лучше не попадаться иначе умрёшь",
              '     2 - Пламя, обычное препятствие, которое мешает пройти', '',
              '  Ваша задача - пройти уровень, собрав наибольшее количество очков']

# Отображаю правила второго уровня
start_screen(intro_text, 'SecondLevelFon.png')
score = SecondLevel.second_level(True, score)

intro_text = ['                             Третий Уровень - Дикий Запад', '', '', '',
              "                                          ПРАВИЛА УРОВНЯ",
              "             Управление игроком -> кнопки WASD или стрелочки",
              '   Чтобы пройти уровень необходимо дойти до верхнего конца', '',
              '                                       Два типа вознаграждения:',
              '                 1 - Мешок с деньгами, 1000 очков',
              '                 2 - Большой мешок с деньгами, нужен ключ, 4000 очков', '',
              '                                             Четыре типа врагов:',
              "     1 - Перекати поле, движутся на вас с огромной скоростью, убьют",
              '     2 - Кактус и Колючий куст, препятствие, которое не даёт пройти',
              '     3 - Ковбой, если наткнуться на него, то умрёшь, стреляет пулями',
              '     4 - Пули, идут чередой с небольшой скоростью, но могут убить', '',
              '  Ваша задача - пройти уровень, собрав наибольшее количество очков']

start_screen(intro_text, 'ThirdLevelFon.png', 'brown')

record: list = ThirdLevel.third_level(True, score)

first_record: str = '                       ' + record[0]
second_record: str = '                       ' + record[1]
third_record: str = '                       ' + record[2]

your_record: str = '                       ' + record[3]

record: list = ['                    Рекорды:', first_record, second_record,
                third_record, '', '                  Ваш результат',
                your_record]

start_screen(record, 'RecordsFon.png', 'yellow', 70)

pygame.quit()
