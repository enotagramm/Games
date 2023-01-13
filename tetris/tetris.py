import pygame
from copy import deepcopy
from random import randrange, choice


# создание игрового поля
W, H = 10, 20
TILE = 40   # Размер плитки
GAME_RES = W * TILE, H * TILE  # размеры рабочего окна (Разрешение)
RES = 800, 820

pygame.init()
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)  # создание рабочего окна
clock = pygame.time.Clock()

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

colors = {
    'grid': (40, 40, 40),
}

figures_position = [[(-1, -1), (-2, -1), (0, -1), (1, -1)],
                    [(0, 0), (-1, 0), (-2, 0), (0, -1)],
                    [(0, 0), (0, 1), (-1, -1), (-1, 0)],
                    [(0, 0), (0, -1), (-1, -1), (-1, 0)],
                    [(0, 0), (0, -1), (-1, 1), (-1, 0)],
                    [(0, 0), (-1, -1), (-1, 0), (1, 0)],
                    [(0, 0), (-1, -1), (0, -1), (1, -1)]]

figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_position]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0] * W for _ in range(H)]

# переменные для падения фигуры
anim_count, anim_speed, anim_limit = 0, 60, 2000

bg = pygame.image.load('img/galaktika_vselennaia_kosmos_138271_800x1280.jpg').convert()
game_bg = pygame.image.load('img/kosmonavt_astronavt_art_134410_540x960.jpg').convert()

main_font = pygame.font.Font('font/retro-land-mayhem.ttf', 80)
font = pygame.font.Font('font/retro-land-mayhem.ttf', 45)

title_tetris = main_font.render('TETRIS', True, pygame.Color('darkblue'))
title_score = font.render('score:', True, pygame.Color('darkorange'))
title_record = font.render('record:', True, pygame.Color('purple'))

get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

FPS = 60

# проверка границ право и лево
def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True

def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')

def set_record(record, score):
    res = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(res))

# каркас программы
while True:
    record = get_record()
    dx, rotate = 0, False
    sc.blit(bg, (0, 0))
    sc.blit(game_sc, (10, 10))
    game_sc.blit(game_bg, (0, 0))
    # game_sc.fill(pygame.Color('black'))
    # для ощущение погруженности делаем задержку
    for i in range(lines):
        pygame.time.wait(200)
    # манипуляция
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_UP:
                rotate = True

    # движение по x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break

    # движение по y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                anim_limit = 2000
                break
    # вращение
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break

    # проверка последней линии
    line, lines = H - 1, 0
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            anim_speed += 3
            lines += 1

    # начисление очков
    score += scores[lines]

    # создание рабочей сетки
    [pygame.draw.rect(game_sc, colors['grid'], i_rect, 1) for i_rect in grid]

    # создание фигуры
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_sc, color, figure_rect)
    # создание всех упавших фигур
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x = x * TILE
                figure_rect.y = y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)

    # cоздание следующей фигуры
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + 410
        figure_rect.y = next_figure[i].y * TILE + 185
        pygame.draw.rect(sc, next_color, figure_rect)

    # создание надписи
    sc.blit(title_tetris, (430, -10))
    sc.blit(title_score, (440, 700))
    sc.blit(font.render(str(score), True, pygame.Color('white')), (630, 701))
    sc.blit(title_record, (440, 650))
    sc.blit(font.render(str(record), True, pygame.Color('white')), (660, 651))

    #конец игры
    for i in range(W):
        if field[0][i]:
            set_record(record, score)
            field = [[0] * W for _ in range(H)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(game_sc, get_color(), i_rect)
                sc.blit(game_sc, (10, 10))
                pygame.display.flip()
                clock.tick(100)

    pygame.display.flip()
    clock.tick(FPS)
# ----------------------------------------------
