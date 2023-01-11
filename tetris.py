import pygame


# создание игрового поля
W, H = 10, 20
TILE = 40   # Размер плитки
GAME_RES = W * TILE, H * TILE  # размеры рабочего окна (Разрешение)

pygame.init()
game_sc = pygame.display.set_mode(GAME_RES)  # создание рабочего окна
clock = pygame.time.Clock()

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

colors = {
    'grid': (90, 40, 40),
}

figures_position = [
    [(), (), (), ()],
    [(), (), (), ()],
    [(), (), (), ()],
    [(), (), (), ()],
    [(), (), (), ()],
    [(), (), (), ()],
    [(), (), (), ()],
]

FPS = 60

# каркас программы
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # создание рабочей сетки
    [pygame.draw.rect(game_sc, colors['grid'], i_rect, 1) for i_rect in grid]


    pygame.display.flip()
    clock.tick(FPS)
# ----------------------------------------------
