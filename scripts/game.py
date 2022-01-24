from constants import screen, fantom_screen, boxes, all_sprites, all_sprites1, all_sprites2, all_sprites3, walls1, \
    platforms, buttons, fantom_all_sprites, walls, clock, FPS, walls2, walls3, levers, acids,\
    CELL_H, CELL_W, WIDTH, HEIGHT
from classes import Player, Wall, Camera, Door, Platform, Box, Button, Lever, Acid, Button_Interface
import pygame


# Функция для ввыода текста на экран
def draw_text(surf, text, size, x, y, color, center=None):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.x, text_rect.y = (x, y)
    if center:
        text_rect.center = x, y
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
def load_levels(level_world):
    door = Door((0, 0))
    map1 = [[int(el) for el in line.strip().split()] for line in
            open(f'../data/levels/level{level_world}/surface1.txt').readlines()]
    map2 = [[int(el) for el in line.strip().split()] for line in
            open(f'../data/levels/level{level_world}/surface2.txt').readlines()]
    map3 = [[int(el) for el in line.strip().split()] for line in
            open(f'../data/levels/level{level_world}/surface3.txt').readlines()]
    for level in range(1, 4):
        for i, line in enumerate(eval(f"map{level}")):
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
    print(levers)
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
def run(level_world):
    all_sprites1.empty()
    all_sprites2.empty()
    all_sprites3.empty()
    walls1.empty()
    walls2.empty()
    walls3.empty()
    platforms.empty()
    levers.empty()
    boxes.empty()
    buttons.empty()
    acids.empty()
    level = 2

    door = load_levels(level_world)
    collision_door = False
    all_sprites = eval(f'all_sprites{level}')
    walls = eval(f'walls{level}')
    fantom_all_sprites = eval(f'all_sprites{level}')

    is_display_settings = 0

    player = Player()
    camera = Camera()

    target = player
    time = 0
    delta_time = 1 / FPS

    while True:
        time += delta_time
        action = False
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ex_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    answer = pause()
                    if answer == 'Выйти':
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
                final_window('Вы проиграли', str(int(time)))
                return 'lose'
        if action and collision_door:
            final_window('Вы выиграли', str(int(time)), level_world)
            return 'win'

        screen.fill('black')
        all_sprites.draw(screen)
        if is_display_settings:
            draw_settings(player, int(clock.get_fps()), level, buttons)
        fantom_screen.fill('darkgray')
        fantom_all_sprites.draw(fantom_screen)
        screen.blit(fantom_screen, (0, 0))
        draw_text(screen, f'Время {int(time // 60)}:{int(time % 60)}', 25, WIDTH - CELL_W * 3, CELL_H, 'white')
        player.draw(screen)
        pygame.display.flip()


def main_menu():
    play = Button_Interface((WIDTH // 2 - CELL_W * 2, HEIGHT // 4), (CELL_W * 4, CELL_H), 'Играть',
                            start_window, screen, 50)
    _help = Button_Interface((WIDTH // 2 - CELL_W * 2, HEIGHT // 3), (CELL_W * 4, CELL_H), 'Помощь',
                            help_, screen, 50)
    ext = Button_Interface((WIDTH // 2 - CELL_W * 2, HEIGHT // 2.4), (CELL_W * 4, CELL_H), 'Выход',
                            ex_exit, screen, 50)
    btns = []
    btns.append(play)
    btns.append(_help)
    btns.append(ext)
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ex_exit()
            if event.type == pygame.MOUSEMOTION:
                for btn in btns:
                    btn.update(pygame.mouse.get_pos(), False)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btns:
                    btn.update(pygame.mouse.get_pos(), True)

        screen.fill('#202020')
        for btn in btns:
            btn.draw()
        pygame.display.flip()


def pause():
    play = Button_Interface((WIDTH // 2 - CELL_W * 2, HEIGHT // 3), (CELL_W * 4, CELL_H),
                            'Продолжить', None, screen, 50)
    ext = Button_Interface((WIDTH // 2 - CELL_W * 2, HEIGHT // 2), (CELL_W * 4, CELL_H), 'Выйти', None, screen, 50)
    btns = []
    btns.append(play)
    btns.append(ext)
    answer = None
    while not answer:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ex_exit()
            if event.type == pygame.MOUSEMOTION:
                for btn in btns:
                    btn.update(pygame.mouse.get_pos(), False)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btns:
                    answer = btn.update(pygame.mouse.get_pos(), True)
                    if answer:
                        break
        for btn in btns:
            btn.draw()
        pygame.display.flip()
    return answer


def final_window(result, time, lev=None):
    if lev:
        open('../data/info_for_programme/levels.txt', 'w').write(str(lev + 1))
    screen.fill('#202020')
    draw_text(screen, result, 180, WIDTH // 2, CELL_H, "white", center=True)
    draw_text(screen, f'Ваше время {time}', 70, WIDTH // 2, CELL_H * 5, 'white', center=True)
    draw_text(screen, 'Нажмите любую кнопку для продолжения', 30, WIDTH // 2, HEIGHT - CELL_H * 2, 'white', center=True)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ex_exit()
            if event.type == pygame.KEYDOWN:
                return


def start_window():
    btns = []
    passed_level = int(open('../data/info_for_programme/levels.txt').read().strip())
    for i in range(5):
        lev = i + 1
        if lev <= passed_level:
            clicable = True
        else:
            clicable = False
        level = Button_Interface((CELL_W * (i + i) + CELL_W, CELL_H * 3),
                                 (CELL_W, CELL_H), str(lev),
                                 run, screen, 30, args=lev, clicable=clicable)
        btns.append(level)
    return_btn = Button_Interface((WIDTH // 2 - CELL_W, HEIGHT * 0.8), (CELL_W * 2, CELL_H), 'Назад', None, screen, 30)
    btns.append(return_btn)
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ex_exit()
            if event.type == pygame.MOUSEMOTION:
                for btn in btns:
                    btn.update(pygame.mouse.get_pos(), False)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btns:
                    answer = btn.update(pygame.mouse.get_pos(), True)
                    if answer == 'Назад':
                        return
                    if answer == 'win':
                        passed_level = int(open('../data/info_for_programme/levels.txt').read().strip())
                        for i in range(5):
                            lev = i + 1
                            if lev <= passed_level:
                                clicable = True
                            else:
                                clicable = False
                            level = Button_Interface((CELL_W * (i + i) + CELL_W, CELL_H * 3),
                                                     (CELL_W, CELL_H), str(lev),
                                                     run, screen, 30, args=lev, clicable=clicable)
                            btns.append(level)
        screen.fill('#202020')
        for btn in btns:
            btn.draw()
        pygame.display.flip()


def help_():
    text = open('../data/info_for_programme/help.txt', encoding='utf-8').read()
    lines = []
    line = ''
    for simbol in text:
        if simbol == '\n':
            lines.append(line)
            line = ''
            continue
        if simbol == '\t':
            line += '    '
            continue
        line += simbol
    len_lines = len(lines)
    height = (HEIGHT - CELL_H * 4) // len_lines
    return_ = Button_Interface((WIDTH - 5 * CELL_W, HEIGHT - CELL_H * 2.5), (CELL_W * 4, CELL_H), 'Назад', None, screen,
                            50)
    btns = []
    btns.append(return_)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ex_exit()
            if event.type == pygame.MOUSEMOTION:
                for btn in btns:
                    btn.update(pygame.mouse.get_pos(), False)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btns:
                    answer = btn.update(pygame.mouse.get_pos(), True)
                    if answer:
                        return
        screen.fill('#202020')
        for i in range(len_lines):
            draw_text(screen, lines[i], 30, CELL_W, (i + 1) * height, 'white')
        for btn in btns:
            btn.draw()
        pygame.display.flip()


def ex_exit():
    exit()


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
    main_menu()
    pygame.quit()