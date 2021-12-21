import pygame

from constants import SPEED_PLAYER, SPEEDJUMP_PLAYER, SIZE_PLAYER, POS_PLAYER, GRAVITY, \
    CELL_H, CELL_W, WIDTH, HEIGHT, PLATFORM_SPEED, PLATFORM_SIZE, all_sprites, walls, boxes


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

    def update(self, walls):
        left, right, up, omit = self.check_buttons() # Определение направления
        if up:
            if self.onGround:
                self.speedy = -self.speed_jump # Если прыжок и мы на земле к скорости по y добавляется энергия
        if left:
            self.speedx = -self.speed # Если влево к скорости по x добавляется энергия
        if right:
            self.speedx = self.speed # Если вправо к скорости по x добавляется энергия
        if not (left or right):
            self.speedx = 0 # Если не вправо и не влево стоять
        if not self.onGround:
            self.speedy += GRAVITY # Если мы не наземле мы падаем
        if self.box and omit:
            self.box.rect.x, self.box.rect.y = self.rect.x + CELL_W, self.rect.y
            all_sprites.add(self.box)
            # walls.add(self.box)
            boxes.add(self.box)
            self.box = None

        self.onGround = False

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
        return left, right, up, omit

    def collide(self, speedx, speedy, walls):
        collide_walls = pygame.sprite.spritecollide(self, walls, False)
        for p in collide_walls: # проходимся по стенам с которыми произошла колизия
            # Если скорость была меньше 0 то равняемся по левому краю стены
            if speedx > 0:
                self.rect.right = p.rect.left
            # Если скорость была больше 0 то равняемся по правому краю стены
            if speedx < 0:
                self.rect.left = p.rect.right
            # Если скорость была больше 0 то равняемся по верхнему краю стены и говорим что мы на земле
            if speedy > 0:
                self.rect.bottom = p.rect.top
                self.onGround = True
                self.speedy = 0
            # Если скорость была меньше 0 то равняемся по нижнему краю стены
            if speedy < 0:
                self.rect.top = p.rect.bottom
                self.speedy = 0


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


class Platform(Wall):
    # Инициализация платформы
    def __init__(self, pos, start, end, direction, active):
        super().__init__(pos)
        self.image = pygame.Surface(PLATFORM_SIZE)
        self.image.fill('blue')
        self.start = start # Начальная точка
        self.end = end # Конечная точка
        self.direction = direction # Направление на x или на y
        self.direction_go = '+' # Направление вперёд или назад
        self.active = active # Едет ли платформа
        self.speed = PLATFORM_SPEED # Скорость платформы

    def update(self):
        # Если платформа активровона
        if self.active:
            # То двигаемся в нужном напрвлении, а затем проверяем не вначале или не в конце ли он
            if self.direction == 'x':
                if self.direction_go == '+':
                    self.rect.x += self.speed
                elif self.direction_go == '-':
                    self.rect.x -= self.speed
                if self.rect.x > self.end[0]:
                    self.direction_go = '-'
                if self.rect.x < self.start[0]:
                    self.direction_go = '+'
            if self.direction == 'y':
                if self.direction_go == '+':
                    self.rect.y += self.speed
                elif self.direction_go == '-':
                    self.rect.y -= self.speed
                if self.rect.y >= self.end[1]:
                    self.direction_go = '-'
                if self.rect.y <= self.start[0]:
                    self.direction_go = '+'


class Box(Wall):
    def __init__(self, pos):
        super().__init__(pos)
        self.image.fill('green')
        self.collision = False

    def update(self):
        if not self.collision:
            self.rect.y += GRAVITY
        self.collision = False
