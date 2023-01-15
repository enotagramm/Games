import pygame

# Создание игрового поля
W, H = 50, 50
# Размер ячейки змеи
snake_tile = 15
# Размеры рабочего поля
GAME_RES = snake_tile * W, snake_tile * H
RES = 1024, 768
# Создание рабочей области
grid = [pygame.Rect(x * snake_tile, y * snake_tile, snake_tile, snake_tile) for x in range(W) for y in range(H)]
# Создание рабочего окна
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()
FPS = 60


# функция отрисовки змейки по виртуальным координатам
def snake_paint_item(x, y):
    pygame.draw.rect(sc, pygame.Color('red'), (x * snake_tile, y * snake_tile,
                                               x * snake_tile, y * snake_tile))
    pygame.draw.rect(sc, pygame.Color('yellow'), (x * snake_tile + 2, y * snake_tile + 2,
                                                  x * snake_tile - 4, y * snake_tile - 4))


pygame.init()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    [pygame.draw.rect(sc, pygame.Color('grey'), i_rect, 1) for i_rect in grid]

    snake_paint_item(1, 1)

    pygame.display.flip()
    clock.tick(FPS)
