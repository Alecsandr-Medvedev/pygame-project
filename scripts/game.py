from constants import screen, fantom_screen, boxes, all_sprites, all_sprites1, all_sprites2, all_sprites3, walls1, \
    platforms, buttons, fantom_all_sprites, walls, clock, FPS, MAP1, MAP2, MAP3, walls2, walls3,\
    CELL_H, CELL_W
from classes import Player, Wall, Camera, Door, Platform, Box, Button
import pygame


# Функция для ввыода текста на экран
def draw_text(surf, text, size, x, y, color):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.x, text_rect.y = (x, y)
    surf.blit(text_surface, text_rect)


# Загрузка платформы
def load_platform(line, j, i, ):
    pos = start = (j * CELL_W, i * CELL_H)
    direction = 'y' if line[j + 2] else 'x'
    active = line[j + 3]
    if direction == 'y':
        end = (j * CELL_W, (i + line[j + 1]) * CELL_H)
    else:
        end = ((j + line[j + 1]) * CELL_W, i * CELL_H)
    platform = Platform(pos, start, end, direction, active)
    return platform


def load_button(line, i, j, door):
    pos = (j * CELL_W, i * CELL_H)
    type = line[j + 1]
    if type == 1:
        btn = Button(pos, door)
    else:
        return
    return btn


# Загрузка уровня
def load_levels():
    door = Door((0, 0))
    count = 0
    for level in range(1, 4):
        for i, line in enumerate(eval(f"MAP{level}")):
            for j, el in enumerate(line):
                if not count:
                    pos = (j * CELL_W, i * CELL_H)
                    if el == 1:
                        wall = Wall(pos)
                        eval(f"all_sprites{level}.add(wall)")
                        eval(f"walls{level}.add(wall)")
                    elif el == 2:
                        door.rect.x, door.rect.y = pos
                        eval(f"all_sprites{level}.add(door)")
                    if el == 3:
                        platform = load_platform(line, j, i)
                        eval(f"walls{level}.add(platform)")
                        eval(f"all_sprites{level}.add(platform)")
                        platforms.add(platform)
                        count = 3
                    if el == 4:
                        box = Box(pos)
                        eval(f"all_sprites{level}.add(box)")
                        boxes.add(box)
                    if el == 5:
                        count = 1
                        btn = load_button(line, i, j, door)
                        eval(f"all_sprites{level}.add(btn)")
                        buttons.add(btn)
                else:
                    count -= 1
    return door


# Загрузка уровня на ругой плоскости
# def load_fantom_level(number):
#     fantom_all_sprites.empty()
#     if number in [1, 2, 3]:
#         if number == 1:
#             map_ = MAP1
#         elif number == 2:
#             map_ = MAP2
#         else:
#             map_ = MAP3
#         count = 0
#         for i, line in enumerate(map_):
#             for j, el in enumerate(line):
#                 if not count:
#                     pos = (j * CELL_W, i * CELL_H)
#                     if el:
#                         wall = Wall(pos)
#                         fantom_all_sprites.add(wall)
#                         if el == 5:
#                             count += 1
#                 else:
#                     count -= 1
#     else:
#         for i, line in enumerate(MAP1):
#             for j in range(len(line)):
#                 pos = (j * CELL_W, i * CELL_H)
#                 wall = Wall(pos)
#                 fantom_all_sprites.add(wall)

#
# def return_shift():
#     if walls:
#         for w in walls:
#             return w.rect.x, w.rect.y
#     else:
#         return 0, 0


# Основной цикл
def run():
    level = 2
    door = load_levels()
    all_sprites = eval(f'all_sprites{level}')
    walls = eval(f'walls{level}')
    fantom_all_sprites = eval(f'all_sprites{level}')
    is_display_settings = 0
    pygame.display.set_caption("Play")
    player = Player()
    camera = Camera()
    collision_door = False
    target = player
    while True:
        get_box = False
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_F1:
                    is_display_settings = (is_display_settings + 1) % 2
                if event.key == pygame.K_q:
                    if level != 1:
                        level -= 1
                        all_sprites = eval(f'all_sprites{level}')
                        walls = eval(f'walls{level}')
                if event.key == pygame.K_e:
                    if level != 3:
                        level += 1
                        all_sprites = eval(f'all_sprites{level}')
                        walls = eval(f'walls{level}')
                if event.key == pygame.K_z:
                    fantom_all_sprites = eval(f'all_sprites{level - 1}')
                if event.key == pygame.K_x:
                    fantom_all_sprites = eval(f'all_sprites{level + 1}')
                if event.key == pygame.K_s:
                    if collision_door and door.active:
                        return
                if event.key == pygame.K_BACKSPACE:
                    get_box = True

        player.update(walls)
        collision_wall = pygame.sprite.spritecollide(player, walls, False)
        collision_door = pygame.sprite.collide_mask(player, door)
        for group in [all_sprites1, all_sprites2, all_sprites3]:
            for sprite in group:
                camera.apply(sprite)
        camera.apply(player)
        camera.update(target)
        platforms.update()
        collision_box = pygame.sprite.spritecollide(player, boxes, False)
        if collision_box and not player.box and get_box:
            pass
            # player.box = collision_box[0]
            # collision_box[0].push_me()
            # collision_box[0].kill()
        collision_boxes = pygame.sprite.groupcollide(boxes, walls, False, False)
        for col in collision_boxes:
            col.collision = True
        boxes.update()
        collision_buttons = pygame.sprite.groupcollide(buttons, walls, False, False)
        for col in collision_buttons:
            col.active = True

        screen.fill('darkgray')
        all_sprites.draw(screen)
        if is_display_settings:
            draw_settings(player, int(clock.get_fps()), collision_wall, level)
        fantom_screen.fill('gray')
        fantom_all_sprites.draw(fantom_screen)
        screen.blit(fantom_screen, (0, 0))
        player.draw(screen)
        pygame.display.flip()


# Служебная функция
def draw_settings(player, fps, walls, level):
    text_1 = f"Позиция игрока: {player.rect.center}"
    text_2 = f"Скорость по x: {player.speedx}"
    text_3 = f"Скорость по y: {player.speedy}"
    text_7 = f"Коробки: {''}"
    text_5 = f"ФПС: {fps}"
    text_4 = f'k'
    text_6 = f'Сдвиг: {""}'
    text_8 = f'Поверхность: {level}'
    draw_text(screen, text_1, 12, 10, 10, 'black')
    draw_text(screen, text_2, 12, 10, 30, 'black')
    draw_text(screen, text_3, 12, 10, 50, 'black')
    draw_text(screen, text_4, 12, 10, 70, 'black')
    draw_text(screen, text_5, 12, 10, 90, 'black')
    draw_text(screen, text_6, 12, 10, 110, 'black')
    draw_text(screen, text_7, 12, 10, 130, 'black')
    draw_text(screen, text_8, 12, 10, 150, 'black')


if __name__ == '__main__':
    pygame.init()
    run()
    pygame.quit()