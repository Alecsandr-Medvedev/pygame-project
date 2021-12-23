from constants import screen, fantom_screen, boxes, all_sprites, platforms, buttons, fantom_all_sprites, walls, clock, FPS, MAP1, MAP2, MAP3,\
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
def load_platform(line, j, i, shift_x, shift_y):
    pos = start = (j * CELL_W - shift_x, i * CELL_H - shift_y)
    direction = 'y' if line[j + 2] else 'x'
    active = line[j + 3]
    if direction == 'y':
        end = (j * CELL_W - shift_x, (i + line[j + 1]) * CELL_H - shift_y)
    else:
        end = ((j + line[j + 1]) * CELL_W - shift_x, i * CELL_H - shift_y)
    platform = Platform(pos, start, end, direction, active)
    return platform


def load_button(line, i, j, shift_x, shift_y, door):
    pos = (j * CELL_W - shift_x, i * CELL_H - shift_y)
    type = line[j + 1]
    if type == 1:
        btn = Button(pos, door)
    all_sprites.add(btn)
    buttons.add(btn)


# Загрузка уровня
def load_level(number, door):
    shift_x, shift_y = map(lambda x: x * -1, return_shift())
    if number == 1:
        map_ = MAP1
    elif number == 2:
        map_ = MAP2
    elif number == 3:
        map_ = MAP3
    else:
        return
    all_sprites.empty()
    walls.empty()
    boxes.empty()
    count = 0
    for i, line in enumerate(map_):
        for j, el in enumerate(line):
            if not count:
                pos = (j * CELL_W - shift_x, i * CELL_H - shift_y)
                if el == 1:
                    wall = Wall(pos)
                    all_sprites.add(wall)
                    walls.add(wall)
                elif el == 2:
                    door.rect.x, door.rect.y = pos
                    all_sprites.add(door)
                if el == 3:
                    platform = load_platform(line, j, i, shift_x, shift_y)
                    walls.add(platform)
                    all_sprites.add(platform)
                    platforms.add(platform)
                    count = 3
                if el == 4:
                    box = Box(pos, number)
                    all_sprites.add(box)
                    boxes.add(box)
                if el == 5:
                    count = 1
                    load_button(line, i, j, shift_x, shift_y, door)
            else:
                count -= 1
    return door


# Загрузка уровня на ругой плоскости
def load_fantom_level(number):
    shift_x = 0
    shift_y = 0
    for sprite in fantom_all_sprites:
        shift_x = -sprite.rect.x
        shift_y = -sprite.rect.y
        break
    fantom_all_sprites.empty()
    if number in [1, 2, 3]:
        if number == 1:
            map_ = MAP1
        elif number == 2:
            map_ = MAP2
        else:
            map_ = MAP3
        count = 0
        for i, line in enumerate(map_):
            for j, el in enumerate(line):
                if not count:
                    pos = (j * CELL_W - shift_x, i * CELL_H - shift_y)
                    if el:
                        wall = Wall(pos)
                        fantom_all_sprites.add(wall)
                        if el == 5:
                            count += 1
                else:
                    count -= 1
    else:
        for i, line in enumerate(MAP1):
            for j in range(len(line)):
                pos = (j * CELL_W - shift_x, i * CELL_H - shift_y)
                wall = Wall(pos)
                fantom_all_sprites.add(wall)


def return_shift():
    if walls:
        for w in walls:
            return w.rect.x, w.rect.y
    else:
        return 0, 0


# Основной цикл
def run():
    door = Door((0, 0))
    level = 2
    door = load_level(level, door)
    load_fantom_level(1)
    is_display_settings = 0
    pygame.display.set_caption("Play")
    player = Player()
    all_sprites.add(player)
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
                        door = load_level(level, door)
                        all_sprites.add(player)
                        load_fantom_level(level - 1)
                if event.key == pygame.K_e:
                    if level != 3:
                        level += 1
                        door = load_level(level, door)
                        all_sprites.add(player)
                        load_fantom_level(level + 1)
                if event.key == pygame.K_z:
                    load_fantom_level(level - 1)
                if event.key == pygame.K_x:
                    load_fantom_level(level + 1)
                if event.key == pygame.K_s:
                    if collision_door and door.active:
                        return
                if event.key == pygame.K_BACKSPACE:
                    get_box = True

        player.update(walls)
        collision_wall = pygame.sprite.spritecollide(player, walls, False)
        collision_door = pygame.sprite.collide_mask(player, door)
        for sprite in all_sprites:
            camera.apply(sprite)
        for sprite in fantom_all_sprites:
            camera.apply(sprite)
        camera.update(target)
        platforms.update()
        collision_box = pygame.sprite.spritecollide(player, boxes, False)
        if collision_box and not player.box and get_box:
            load_fantom_level(level - 1)
            player.box = collision_box[0]
            collision_box[0].push_me(*return_shift())
            collision_box[0].kill()
        collision_boxes = pygame.sprite.groupcollide(boxes, walls, False, False)
        for col in collision_boxes:
            col.collision = True
        boxes.update(*return_shift())
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
        pygame.display.flip()


# Служебная функция
def draw_settings(player, fps, walls, level):
    text_1 = f"Позиция игрока: {player.rect.center}"
    text_2 = f"Скорость по x: {player.speedx}"
    text_3 = f"Скорость по y: {player.speedy}"
    text_7 = f"Коробки: {[(b.x, b.y) for b in boxes]}"
    text_5 = f"ФПС: {fps}"
    text_4 = f'k'
    text_6 = f'Сдвиг: {return_shift()}'
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
