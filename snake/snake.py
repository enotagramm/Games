import pygame
from random import randrange

# Создание игрового поля
W, H = 50, 50
# Размер ячейки змеи
snake_tile = 15
# Размеры рабочего поля
GAME_RES = snake_tile * W, snake_tile * H
RES = 1024, 768
# Создание рабочей области
# grid = [pygame.Rect(x * snake_tile, y * snake_tile, snake_tile, snake_tile) for x in range(W) for y in range(H)]
# Создание рабочего окна
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()
FPS = 60
# определение позиции змейки
snake_x = 24
snake_y = 24
# список хранения координат змеи
snake_list = []
snake_size = 3
anim_count, anim_speed, anim_limit = 0, 60, 500
move = {'move_up': False, 'move_down': False, 'move_left': False, 'move_right': False}
# добыча
food_set = []
food_size = 50
for i in range(food_size):
    while len(food_set) < food_size:
        x, y = randrange(W), randrange(H)
        if x != snake_x and y != snake_y:
            radius = snake_tile / 2
            food = pygame.draw.circle(game_sc, pygame.Color('red'),
                                      (x * snake_tile + radius, y * snake_tile + radius), radius)
            if (x, y, food) not in food_set:
                food_set.append((x, y, food))


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
    for item in snake_list:
        x, y, *id_1_2 = item
        if f_x == x and f_y == y:
            return False
    return True


def check_food():
    global snake_size, food_set, anim_speed
    for item in food_set:
        x, y, food = item
        if x == snake_x and y == snake_y:
            snake_size += 1
            anim_speed += 10
            game_sc.fill(pygame.Color('red'), rect=food)
            food_set.remove(item)

snake_x_nav = 0
snake_y_nav = 0


pygame.init()

while True:
    sc.blit(game_sc, (10, 10))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not move['move_down']:
                for x in move:
                    if x == 'move_up':
                        move[x] = True
                        snake_y_nav = -1
                        snake_x_nav = 0
                    else:
                        move[x] = False
            if event.key == pygame.K_DOWN and not move['move_up']:
                for x in move:
                    if x == 'move_down':
                        move[x] = True
                        snake_y_nav = 1
                        snake_x_nav = 0
                    else:
                        move[x] = False
            if event.key == pygame.K_LEFT and not move['move_right']:
                for x in move:
                    if x == 'move_left':
                        move[x] = True
                        snake_x_nav = -1
                        snake_y_nav = 0
                    else:
                        move[x] = False
            if event.key == pygame.K_RIGHT and not move['move_left']:
                for x in move:
                    if x == 'move_right':
                        move[x] = True
                        snake_x_nav = 1
                        snake_y_nav = 0
                    else:
                        move[x] = False
    # move

    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        for x in move:
            if move[x] and check_snake(snake_x + snake_x_nav, snake_y + snake_y_nav):
                snake_x += snake_x_nav
                snake_y += snake_y_nav
                # if x == 'move_up':
                #     snake_y +
                # if x == 'move_down':
                #     snake_y += 1
                # if x == 'move_left':
                #     snake_x -= 1
                # if x == 'move_right':
                #     snake_x += 1

    snake_paint_item(snake_x, snake_y)
    check_snake_size()
    check_food()
    check_borders()

    pygame.display.flip()
    clock.tick(FPS)
