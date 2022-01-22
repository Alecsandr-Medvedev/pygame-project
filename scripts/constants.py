import os
import sys

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
MAP1 = [[int(el) for el in line.strip().split()] for line in open('../data/levels/level1/surface1.txt').readlines()]
MAP2 = [[int(el) for el in line.strip().split()] for line in open('../data/levels/level1/surface2.txt').readlines()]
MAP3 = [[int(el) for el in line.strip().split()] for line in open('../data/levels/level1/surface3.txt').readlines()]
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
levers = pygame.sprite.Group()
boxes = pygame.sprite.Group()
buttons = pygame.sprite.Group()
acids = pygame.sprite.Group()

screen = pygame.display.set_mode((WIDTH, (HEIGHT - 60)))
fantom_screen = pygame.display.set_mode((WIDTH, (HEIGHT - 60)))
fantom_screen = fantom_screen.convert(screen)
fantom_screen.set_alpha(50)
# Параметры игрока
SPEED_PLAYER = 6
SPEEDJUMP_PLAYER = 50
SIZE_PLAYER = (CELL_W, CELL_H * 2)
POS_PLAYER = WIDTH // 2, HEIGHT // 2
MAX_SPEED = 40
PUSH = FRICTION * 3
# Параметры платформы
PLATFORM_COUNT = 15
PLATFORM_SPEED = CELL_W // PLATFORM_COUNT


def load_image(name, place='img', colorkey=None):
    f = os.path.abspath('')
    fullname = f[:-7] + os.path.join('data', place, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


wall_img = pygame.transform.scale(load_image('Wall.png'), (CELL_W, CELL_H))
acid_img = pygame.transform.scale(load_image('Acid.png'), (CELL_W, CELL_H))
box_img = pygame.transform.scale(load_image('Box.png'), (CELL_W, CELL_H))
button_down_img = pygame.transform.scale(load_image('ButtonDown.png'), (CELL_W, CELL_H))
button_up_img = pygame.transform.scale(load_image('ButtonUp.png'), (CELL_W, CELL_H))
lever_up_img = pygame.transform.scale(load_image('LeverUp.png'), (CELL_W, CELL_H))
lever_down_img = pygame.transform.scale(load_image('LeverDown.png'), (CELL_W, CELL_H))
platform_img = load_image('Platform.png')
door_lock_img = pygame.transform.scale(load_image('DoorLock.png'), (CELL_W, CELL_H * 2))
door_open_img = pygame.transform.scale(load_image('DoorOpen.png'), (CELL_W, CELL_H * 2))

