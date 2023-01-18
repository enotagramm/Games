import pygame
from random import randrange

# Создание игрового поля
W, H = 50, 50
# Размер ячейки змеи
snake_tile = 15
# Размеры рабочего поля
GAME_RES = snake_tile * W, snake_tile * H
RES = 1024, 768

FPS = 60
# определение позиции змейки
snake_x = 24
snake_y = 24
# движение змеи
snake_x_nav = 0
snake_y_nav = 0
# Окончание игры
GAME_OVER = False
# список хранения координат змеи
snake_list = []
snake_size = 3
# переменные для движения змеи
anim_count, anim_speed, anim_limit = 0, 60, 500
steps = {'K_UP': False, 'K_DOWN': False, 'K_LEFT': False, 'K_RIGHT': False}
# добыча
food_set = tuple()
# очки
score = 0
# цвета
game_bg = (104, 20, 130)

pygame.init()
# Создание сетки
# grid = [pygame.Rect(x * snake_tile, y * snake_tile, snake_tile, snake_tile) for x in range(W) for y in range(H)]
# Создание рабочего окна
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()
pygame.display.set_caption("Пожиратель")

bg = pygame.image.load('img/fioletovyy_sploshnoy_fon_krasochnyy_65843_1024x768.jpg').convert()
game_sc.fill(game_bg)

main_font = pygame.font.Font('font/dash-pixel-7.ttf', 45)
font = pygame.font.Font('font/dash-pixel-7.ttf', 35)

title_snake = main_font.render('DEVOURER', True, pygame.Color('black'))
title_score = font.render('score', True, pygame.Color('black'))
title_record = font.render('record', True, pygame.Color('black'))


def food_snake():
    global food_set
    while 1:
        x, y = randrange(W), randrange(H)
        if x != snake_x and y != snake_y:
            radius = snake_tile / 2
            food = pygame.draw.circle(game_sc, pygame.Color('yellow'),
                                      (x * snake_tile + radius, y * snake_tile + radius), radius)
            if (x, y, food) not in food_set:
                food_set += (x, y, food)
                return food


# функция отрисовки змейки по виртуальным координатам
def snake_paint_item(x, y):
    global snake_list
    id1 = pygame.draw.rect(game_sc, pygame.Color('red'), (x * snake_tile, y * snake_tile,
                                                          snake_tile, snake_tile))

    id2 = pygame.draw.rect(game_sc, pygame.Color('yellow'), (x * snake_tile + 2, y * snake_tile + 2,
                                                             snake_tile - 4, snake_tile - 4))
    if [x, y, id1, id2] not in snake_list:
        snake_list.append([x, y, id1, id2])


def check_snake_size():
    if len(snake_list) > snake_size:
        temp_item = snake_list.pop(0)
        game_sc.fill(pygame.Color('black'), rect=temp_item[2])


def check_borders():
    global snake_x, snake_y
    if snake_x > W:
        snake_x = 0
    if snake_x < 0:
        snake_x = W
    if snake_y > H:
        snake_y = 0
    if snake_y < 0:
        snake_y = H


def check_snake(f_x, f_y):
    global GAME_OVER
    for item in snake_list:
        x, y, *id_1_2 = item
        if f_x == x and f_y == y:
            GAME_OVER = True
            # add_record(record, score)
            return False
    return True


def check_food():
    global snake_size, food_set, anim_speed, score
    x, y, food = food_set
    if x == snake_x and y == snake_y:
        snake_size += 1
        anim_speed += 10
        score += 100
        game_sc.fill(pygame.Color('red'), rect=food)
        food_set = tuple()


def keyboard_move(nav):
    global steps
    for move in steps:
        if move == nav:
            steps[move] = True
        else:
            steps[move] = False


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def add_record(record, score):
    result = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(result))


while True:
    record = get_record()
    sc.blit(bg, (0, 0))
    sc.blit(game_sc, (10, 10))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if not GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not steps['K_DOWN']:
                    keyboard_move('K_UP')
                    snake_y_nav = -1
                    snake_x_nav = 0
                if event.key == pygame.K_DOWN and not steps['K_UP']:
                    keyboard_move('K_DOWN')
                    snake_y_nav = 1
                    snake_x_nav = 0
                if event.key == pygame.K_LEFT and not steps['K_RIGHT']:
                    keyboard_move('K_LEFT')
                    snake_x_nav = -1
                    snake_y_nav = 0
                if event.key == pygame.K_RIGHT and not steps['K_LEFT']:
                    keyboard_move('K_RIGHT')
                    snake_x_nav = 1
                    snake_y_nav = 0

    # move
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        for move in steps:
            if steps[move] and check_snake(snake_x + snake_x_nav, snake_y + snake_y_nav):
                snake_x += snake_x_nav
                snake_y += snake_y_nav
    # food
    if len(food_set) == 0:
        food_snake()

    snake_paint_item(snake_x, snake_y)
    check_snake_size()
    check_food()
    check_borders()

    sc.blit(title_snake, (775, 10))
    sc.blit(title_score, (835, 600))
    sc.blit(title_record, (820, 500))
    sc.blit(font.render(str(score), True, pygame.Color('black')), (854, 650))
    sc.blit(font.render(str(record), True, pygame.Color('black')), (854, 540))
    pygame.display.flip()
    clock.tick(FPS)
