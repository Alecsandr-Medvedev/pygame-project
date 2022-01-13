from constants import screen, fantom_screen, boxes, all_sprites, all_sprites1, all_sprites2, all_sprites3, walls1, \
    platforms, buttons, fantom_all_sprites, walls, clock, FPS, MAP1, MAP2, MAP3, walls2, walls3, levers,\
    CELL_H, CELL_W
from classes import Player, Wall, Camera, Door, Platform, Box, Button, Lever
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
def load_platform(el, pos):
    el = list(map(int, [e for e in el]))
    direction = 'y' if el[1] else 'x'
    active = el[2]
    len_ = el[3]
    size = el[4]
    id_ = el[5]
    platform = Platform(pos, len_, direction, active, size, id_)
    return platform


def load_button(el, door, pos):
    type = el[1]
    if type == '0':
        btn = Button(pos, door=door)
    else:
        btn = Button(pos, _id=int(type))
    return btn


# Загрузка уровня
def load_levels():
    door = Door((0, 0))
    for level in range(1, 4):
        for i, line in enumerate(eval(f"MAP{level}")):
            for j, el in enumerate(line):
                pos = (j * CELL_W, i * CELL_H)
                if el < 9:
                    if el == 1:
                        wall = Wall(pos)
                        eval(f"all_sprites{level}.add(wall)")
                        eval(f"walls{level}.add(wall)")
                    elif el == 2:
                        door.rect.x, door.rect.y = pos
                        eval(f"all_sprites{level}.add(door)")
                    elif el == 4:
                        box = Box(pos, level)
                        eval(f"all_sprites{level}.add(box)")
                        # eval(f"walls{level}.add(box)")
                        boxes.add(box)
                else:
                    el = str(el)
                    if el[0] == '3':
                        platform = load_platform(el, pos)
                        eval(f"walls{level}.add(platform)")
                        eval(f"all_sprites{level}.add(platform)")
                        platforms.add(platform)
                    if el[0] == '5':
                        btn = load_button(el, door, pos)
                        eval(f"all_sprites{level}.add(btn)")
                        buttons.add(btn)
                    if el[0] == '6':
                        lever = Lever(pos, int(el[1]))
                        eval(f"all_sprites{level}.add(platform)")
                        levers.add(lever)

    for btn in buttons:
        if btn.id:
            for plat in platforms:
                if plat.id == btn.id:
                    btn.platform = plat
    return door


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

        player.update(walls)
        collision_door = pygame.sprite.collide_mask(player, door)
        for group in [all_sprites1, all_sprites2, all_sprites3]:
            for sprite in group:
                camera.apply(sprite)
        camera.apply(player)
        camera.update(target)
        platforms.update()
        collision_box = pygame.sprite.spritecollide(player, boxes, False)
        if collision_box and not player.box and player.get_box:
            player.box = collision_box[0]
            collision_box[0].kill()
        if player.box and player.omit:
            shift = -CELL_W if player.last_direction == 'left' else CELL_W
            player.box.rect.x, player.box.rect.y, player.box.level = player.rect.x + shift, player.rect.y, level
            all_sprites.add(player.box)
            boxes.add(player.box)
            player.box = None
        for box in boxes:
            collision_boxes = pygame.sprite.spritecollide(box, eval(f'walls{box.level}'), False)
            if collision_boxes:
                box.collision = True
        boxes.update()
        for button in buttons:
            collision_button_1 = pygame.sprite.spritecollide(button, boxes, False)
            collision_button_2 = pygame.sprite.collide_mask(button, player)
            if collision_button_1 or collision_button_2:
                button.activate(True)
            else:
                button.activate(False)
        collision_platforms = pygame.sprite.spritecollide(player, platforms, False)
        if collision_platforms:
            player.speedy += collision_platforms[0].speed

        screen.fill('darkgray')
        all_sprites.draw(screen)
        if is_display_settings:
            draw_settings(player, int(clock.get_fps()), level)
        fantom_screen.fill('gray')
        fantom_all_sprites.draw(fantom_screen)
        screen.blit(fantom_screen, (0, 0))
        player.draw(screen)
        pygame.display.flip()


# Служебная функция
def draw_settings(player, fps, level):
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