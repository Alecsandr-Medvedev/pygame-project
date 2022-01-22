import pygame

from constants import SPEED_PLAYER, SPEEDJUMP_PLAYER, SIZE_PLAYER, POS_PLAYER, PUSH, MAX_SPEED, GRAVITY, FRICTION, \
    CELL_H, CELL_W, WIDTH, HEIGHT, PLATFORM_SPEED, PLATFORM_COUNT, wall_img, acid_img, box_img, button_down_img,\
    button_up_img, lever_up_img, lever_down_img, platform_img, door_lock_img, door_open_img


# Создание игрока
class Player(pygame.sprite.Sprite):
    # Иницализация
    def __init__(self):
        super().__init__()
        self.speedx = 0  # Скорость по x
        self.speedy = 0  # Скорость по y
        self.onGround = False # Положение на земле
        self.image = pygame.Surface(SIZE_PLAYER) # Игрок
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = POS_PLAYER # Позиция игрока
        self.speed_jump = SPEEDJUMP_PLAYER # Скорость прышка игрока
        self.speed = SPEED_PLAYER # Скорость игрока
        self.box = None # Есть ли у игрока коробка
        self.last_direction = 'right'

    def update(self, walls):
        left, right, up = self.check_buttons() # Определение направления
        if up:
            if self.onGround:
                self.speedy = -self.speed_jump # Если прыжок и мы на земле к скорости по y добавляется энергия
        if left:
            self.speedx += -self.speed # Если влево к скорости по x добавляется энергия
        if right:
            self.speedx += self.speed # Если вправо к скорости по x добавляется энергия
        if self.speedx > 0:
            self.speedx -= FRICTION
        elif self.speedx < 0:
            self.speedx += FRICTION # Торможение
        if abs(self.speedx) < FRICTION:
            self.speedx = 0 # Для предотвращения дергания
        if not self.onGround:
            self.speedy += GRAVITY # Если мы не наземле мы падаем
        if abs(self.speedx) > MAX_SPEED:
            if self.speedx > 0:
                self.speedx = MAX_SPEED
            if self.speedx < 0:
                self.speedx = -MAX_SPEED
        self.onGround = False
        if self.speedx > 0:
            self.last_direction = 'right'
        elif self.speedx < 0:
            self.last_direction = 'left'

        self.rect.y += self.speedy # Прибавляем к положению игрока его скорость
        self.collide(0, self.speedy, walls) # Проверка на столкновения

        self.rect.x += self.speedx # Прибавляем к положению игрока его скорость
        self.collide(self.speedx, 0, walls) # Проверка на столкновения

    def check_buttons(self):
        # Проверка на нажатие нужных кнопок
        key = pygame.key.get_pressed()
        left = False
        right = False
        up = False
        if key[pygame.K_a]:
            left = True
        if key[pygame.K_d]:
            right = True
        if key[pygame.K_w]:
            up = True
        return left, right, up

    def collide(self, speedx, speedy, walls):
        collide_walls = pygame.sprite.spritecollide(self, walls, False)
        if collide_walls: # проходимся по стенам с которыми произошла колизия
            p = collide_walls[0]
            # Если скорость была меньше 0 то равняемся по левому краю стены
            if speedx > 0:
                self.rect.right = p.rect.left
                self.speedx -= PUSH
            # Если скорость была больше 0 то равняемся по правому краю стены
            elif speedx < 0:
                self.rect.left = p.rect.right
                self.speedx += PUSH
            # Если скорость была больше 0 то равняемся по верхнему краю стены и говорим что мы на земле
            if speedy > 0:
                self.rect.bottom = p.rect.top
                self.onGround = True
                self.speedy = 0
            # Если скорость была меньше 0 то равняемся по нижнему краю стены
            if speedy < 0:
                self.rect.top = p.rect.bottom
                self.speedy = 0

    def draw(self, surface):
        pygame.draw.rect(surface, 'black', self.rect)


class Wall(pygame.sprite.Sprite):
    # Инициализация стены
    def __init__(self, pos):
        super().__init__()
        self.image = wall_img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


class Camera:
    # Иницализация камеры
    def __init__(self):
        self.dx = 0 # Смещение по x
        self.dy = 0 # Смещение по y

    def apply(self, obj):
        # Смещаем объект
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2) # Устанавливаем смещение по x
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2) # Устанавливаем смещение по y


class Door(Wall):
    # Инициализация двери
    def __init__(self, pos):
        super().__init__(pos)
        self.active = 0
        self.images = [door_lock_img, door_open_img]
        self.image = self.images[self.active]

    def change_image(self):
        self.image = self.images[self.active]


class Platform(pygame.sprite.Sprite):
    # Инициализация платформы
    def __init__(self, pos, len_way, direction, active, size, id_):
        super().__init__()
        self.image = pygame.transform.scale(platform_img, (CELL_W * size, CELL_H))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.direction = direction # Направление на x или на y
        self.direction_go = '+' # Направление вперёд или назад
        self.active = active # Едет ли платформа
        self.speed = PLATFORM_SPEED # Скорость платформы
        self.len_way = int(len_way)
        self.passed_way = 0
        self.count = 1 / PLATFORM_COUNT
        self.id = id_

    def update(self):
        # Если платформа активровона
        if self.active:
            # То двигаемся в нужном напрвлении, а затем проверяем не вначале или не в конце ли он
            self.last_go = pygame.time.get_ticks()
            if self.direction == 'x':
                self.rect.x += self.speed
            if self.direction == 'y':
                self.rect.y += self.speed
            self.passed_way += self.count
            if self.passed_way >= self.len_way:
                self.passed_way = 0
                self.speed *= -1


class Box(Wall):
    def __init__(self, pos, level):
        super().__init__(pos)
        self.image = box_img
        self.collision = False
        self.level = level

    def update(self):
        if not self.collision:
            self.rect.y += GRAVITY
        self.collision = False

    def push_me(self):
        pass


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, level, door=None, _id=None):
        super().__init__()
        self.image = button_up_img
        self.rect = self.image.get_rect()
        self.colors = [button_up_img, button_down_img]
        self.rect.x, self.rect.y = pos
        self.door = door
        self.id = _id
        self.platform = None
        self.level = level

    def activate(self, active):
        if self.door:
            self.door.active = active
            self.door.change_image()
        else:
            self.platform.active = active
        self.image = self.colors[active]


class Lever(Button):
    def __init__(self, pos, level, _id):
        super().__init__(pos, level, _id=_id)
        self.image = lever_down_img
        self.colors = [lever_down_img, lever_up_img]
        self.active = 0

    def activated(self):
        self.active = (self.active + 1) % 2
        self.platform.active = self.active
        self.image = self.colors[self.active]


class Acid(Wall):
    def __init__(self, pos, level):
        super().__init__(pos)
        self.image = acid_img
        self.level = level

