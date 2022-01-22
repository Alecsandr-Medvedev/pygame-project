from constants import screen, fantom_screen, boxes, all_sprites, all_sprites1, all_sprites2, all_sprites3, walls1, \
    platforms, buttons, fantom_all_sprites, walls, clock, FPS, MAP1, MAP2, MAP3, walls2, walls3, levers, acids,\
    CELL_H, CELL_W
from classes import Player, Wall, Camera, Door, Platform, Box, Button, Lever, Acid
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


def load_button(el, door, pos, level):
    type = el[1]
    if type == '0':
        btn = Button(pos, level, door=door)
    else:
        btn = Button(pos, level, _id=int(type))
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
                    elif el == 7:
                        acid = Acid(pos, level)
                        eval(f"all_sprites{level}.add(acid)")
                        acids.add(acid)
                else:
                    el = str(el)
                    if el[0] == '3':
                        platform = load_platform(el, pos)
                        eval(f"walls{level}.add(platform)")
                        eval(f"all_sprites{level}.add(platform)")
                        platforms.add(platform)
                    if el[0] == '5':
                        btn = load_button(el, door, pos, level)
                        eval(f"all_sprites{level}.add(btn)")
                        buttons.add(btn)
                    if el[0] == '6':
                        lever = Lever(pos, int(el[1]), level)
                        eval(f"all_sprites{level}.add(lever)")
                        levers.add(lever)

    for btn in buttons:
        if btn.id:
            for plat in platforms:
                if plat.id == btn.id:
                    btn.platform = plat
    for lever in levers:
        if lever.id:
            for plat in platforms:
                if plat.id == lever.id:
                    lever.platform = plat
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

    target = player
    while True:
        action = False
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
                        fantom_all_sprites = eval(f'all_sprites{level}')
                if event.key == pygame.K_e:
                    if level != 3:
                        level += 1
                        all_sprites = eval(f'all_sprites{level}')
                        walls = eval(f'walls{level}')
                        fantom_all_sprites = eval(f'all_sprites{level}')
                if event.key == pygame.K_z:
                    if level != 1:
                        fantom_all_sprites = eval(f'all_sprites{level - 1}')
                if event.key == pygame.K_x:
                    if level != 3:
                        fantom_all_sprites = eval(f'all_sprites{level + 1}')
                if event.key == pygame.K_RSHIFT:
                    action = True

        player.update(walls)
        if door.active:
            collision_door = pygame.sprite.collide_mask(player, door)
        for group in [all_sprites1, all_sprites2, all_sprites3]:
            for sprite in group:
                camera.apply(sprite)
        camera.apply(player)
        camera.update(target)
        platforms.update()
        if not player.box and action:
            collision_box = pygame.sprite.spritecollide(player, boxes, False)
            for col in collision_box:
                if col.level == level:
                    player.box = col
                    col.kill()
                    action = False
        if player.box and action:
            shift = -CELL_W if player.last_direction == 'left' else CELL_W
            player.box.rect.x, player.box.rect.y, player.box.level = player.rect.x + shift, player.rect.y, level
            all_sprites.add(player.box)
            boxes.add(player.box)
            player.box = None
            action = False
        for box in boxes:
            collision_boxes = pygame.sprite.spritecollide(box, eval(f'walls{box.level}'), False)
            if collision_boxes:
                box.collision = True
        boxes.update()
        for button in buttons:
            if button.level == level:
                collision_button_1 = pygame.sprite.collide_mask(button, player)
            else:
                collision_button_1 = False
            collision_button_2 = pygame.sprite.spritecollide(button, boxes, False)
            for col in collision_button_2:
                if col.level == button.level:
                    col_2 = True
                    break
            else:
                col_2 = False
            if collision_button_1 or col_2:
                button.activate(1)
            else:
                button.activate(0)
        if action:
            collision_levers = pygame.sprite.spritecollide(player, levers, False)
            for col in collision_levers:
                if col.level == level:
                    col.activated()
        collision_acids = pygame.sprite.spritecollide(player, acids, False)
        for col in collision_acids:
            if col.level == level:
                print('you died')
                return
        if action and collision_door:
            print(collision_door)
            return

        screen.fill('black')
        all_sprites.draw(screen)
        if is_display_settings:
            draw_settings(player, int(clock.get_fps()), level, buttons)
        fantom_screen.fill('darkgray')
        fantom_all_sprites.draw(fantom_screen)
        screen.blit(fantom_screen, (0, 0))
        player.draw(screen)
        pygame.display.flip()


# Служебная функция
def draw_settings(player, fps, level, level_b):
    text_1 = f"Позиция игрока: {player.rect.center}"
    text_2 = f"Скорость по x: {player.speedx}"
    text_3 = f"Скорость по y: {player.speedy}"
    text_7 = f"fdsd: {[a.level for a in level_b]}"
    text_5 = f"ФПС: {fps}"
    text_4 = f'k'
    text_6 = f'Сдвиг: {""}'
    text_8 = f'Поверхность: {level}'
    draw_text(screen, text_1, 12, 10, 10, 'white')
    draw_text(screen, text_2, 12, 10, 30, 'white')
    draw_text(screen, text_3, 12, 10, 50, 'white')
    draw_text(screen, text_4, 12, 10, 70, 'white')
    draw_text(screen, text_5, 12, 10, 90, 'white')
    draw_text(screen, text_6, 12, 10, 110, 'white')
    draw_text(screen, text_7, 12, 10, 130, 'white')
    draw_text(screen, text_8, 12, 10, 150, 'white')


if __name__ == '__main__':
    pygame.init()
    run()
    pygame.quit()