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
# добыча
food_list = set()
food_size = 5
for i in range(food_size):
    while len(food_list) < food_size:
        x, y = randrange(W), randrange(H)
        if x != snake_x and y != snake_y:
            radius = snake_tile / 2
            id1 = pygame.draw.circle(game_sc, pygame.Color('red'),
                                     (x * snake_tile + radius, y * snake_tile + radius), radius)
            food_list.add((x, y, id1))


# функция отрисовки змейки по виртуальным координатам
def snake_paint_item(x, y):
    global snake_list
    id1 = pygame.draw.rect(game_sc, pygame.Color('red'), (x * snake_tile, y * snake_tile,
                                                          snake_tile, snake_tile))

    id2 = pygame.draw.rect(game_sc, pygame.Color('yellow'), (x * snake_tile + 2, y * snake_tile + 2,
                                                             snake_tile - 4, snake_tile - 4))
    if [x, y, id1, id2] not in snake_list:
        snake_list.append([x, y, id1, id2])
        print(snake_list)


def check_snake():
    if len(snake_list) >= snake_size:
        temp_item = snake_list.pop(0)
        game_sc.fill(pygame.Color('black'), rect=temp_item[2])


pygame.init()

while True:
    sc.blit(game_sc, (10, 10))
    snake_x_nav = snake_y_nav = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake_y_nav = -1
                check_snake()
            if event.key == pygame.K_DOWN:
                snake_y_nav = 1
                check_snake()
            if event.key == pygame.K_LEFT:
                snake_x_nav = -1
                check_snake()
            if event.key == pygame.K_RIGHT:
                snake_x_nav = 1
                check_snake()


    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_UP]:
    #     snake_y_nav = -1
    #     check_snake()
    # if keys[pygame.K_DOWN]:
    #     snake_y_nav = 1
    #     check_snake()
    # if keys[pygame.K_LEFT]:
    #     snake_x_nav = -1
    #     check_snake()
    # if keys[pygame.K_RIGHT]:
    #     snake_x_nav = 1
    #     check_snake()

    # [pygame.draw.rect(game_sc, pygame.Color('grey'), i_rect, 1) for i_rect in grid]

    snake_x += snake_x_nav
    snake_y += snake_y_nav
    snake_paint_item(snake_x, snake_y)

    pygame.display.flip()
    clock.tick(FPS)
