import pygame

from constants import SPEED_PLAYER, SPEEDJUMP_PLAYER, SIZE_PLAYER, POS_PLAYER, PUSH, MAX_SPEED, GRAVITY, FRICTION, \
    CELL_H, CELL_W, WIDTH, HEIGHT, PLATFORM_SPEED, PLATFORM_COUNT


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
        self.omit = False
        self.get_box = False
        self.last_direction = 'right'

    def update(self, walls):
        left, right, up, omit, get_box = self.check_buttons() # Определение направления
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

        self.omit = omit
        self.get_box = get_box
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
        if key[pygame.K_a]:
            left = True
        else:
            left = False
        if key[pygame.K_d]:
            right = True
        else:
            right = False
        if key[pygame.K_w]:
            up = True
        else:
            up = False
        if key[pygame.K_RSHIFT]:
            omit = True
        else:
            omit = False
        if key[pygame.K_BACKSPACE]:
            get_box = True
        else:
            get_box = False
        return left, right, up, omit, get_box

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
        self.image = pygame.Surface((CELL_W, CELL_H))
        self.image.fill('red')
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
        self.image = pygame.Surface(SIZE_PLAYER)
        self.image.fill('darkred')
        self.active = False


class Platform(pygame.sprite.Sprite):
    # Инициализация платформы
    def __init__(self, pos, len_way, direction, active, size, id_):
        self.image = pygame.Surface((CELL_W * size, CELL_H))
        super().__init__()
        self.image.fill('blue')
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
        self.image.fill('green')
        self.collision = False
        self.level = level

    def update(self):
        if not self.collision:
            self.rect.y += GRAVITY
        self.collision = False

    def push_me(self):
        pass


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, door=None, _id=None):
        super().__init__()
        self.image = pygame.Surface((CELL_W // 2, CELL_H // 2))
        self.image.fill('yellow')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0] + CELL_W // 2, pos[1] + CELL_H // 2
        self.door = door
        self.id = _id
        self.platform = None

    def activate(self, active):
        if self.door:
            self.door.active = active
        else:
            self.platform.active = active


class Lever(Button):
    def __init__(self, pos, _id):
        super().__init__(pos, _id=_id)
        self.colors = ['orange', 'purple']
        self.active = 0
        self.image = pygame.Surface((CELL_W // 2, CELL_H))
        self.image.fill(self.colors[self.active])

    def activated(self):
        self.active = (self.active + 1) % 2
        self.activate(self.active)
        self.image.fill(self.colors[self.active])

