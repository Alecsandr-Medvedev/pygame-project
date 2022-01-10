import pygame
# Создание основных прарметров игры
pygame.init()
# Параметры окна
infoObject = pygame.display.Info()
WIDTH = infoObject.current_w
HEIGHT = infoObject.current_h
FRICTION = 3
CELL_W = 60
CELL_H = 60
FPS = 60
GRAVITY = 3
MAP1 = [[int(el) for el in line.strip()] for line in open('../data/levels/level1/surface1.txt').readlines()]
MAP2 = [[int(el) for el in line.strip()] for line in open('../data/levels/level1/surface2.txt').readlines()]
MAP3 = [[int(el) for el in line.strip()] for line in open('../data/levels/level1/surface3.txt').readlines()]
# Параметры игровго цикла
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
fantom_all_sprites = pygame.sprite.Group()
all_sprites1 = pygame.sprite.Group()
all_sprites2 = pygame.sprite.Group()
all_sprites3 = pygame.sprite.Group()
walls = pygame.sprite.Group()
walls1 = pygame.sprite.Group()
walls2 = pygame.sprite.Group()
walls3 = pygame.sprite.Group()
platforms = pygame.sprite.Group()
boxes = pygame.sprite.Group()
buttons = pygame.sprite.Group()

screen = pygame.display.set_mode((WIDTH, (HEIGHT - 60)))
fantom_screen = pygame.display.set_mode((WIDTH, (HEIGHT - 60)))
fantom_screen = fantom_screen.convert(screen)
fantom_screen.set_alpha(50)
# Параметры игрока
SPEED_PLAYER = 8
SPEEDJUMP_PLAYER = 50
SIZE_PLAYER = (CELL_W, CELL_H * 2)
POS_PLAYER = WIDTH // 2, HEIGHT // 2
MAX_SPEED = 40
PUSH = FRICTION * 3
# Параметры платформы
PLATFORM_SPEED = CELL_W // 6
PLATFORM_SIZE = (CELL_W * 5, CELL_H)
