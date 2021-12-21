import pygame
from random import randrange


class Ball():
    def __init__(self, pos):
        super().__init__()
        self.grad = 255
        self.last_ = pygame.time.get_ticks()
        self.speed = randrange(70, 140)
        self.color = (randrange(255), randrange(255), randrange(255))
        self.pos = pos

    def update(self, all_sprites):
        if pygame.time.get_ticks() - self.last_ >= self.speed:
            self.last_ = pygame.time.get_ticks()
            self.grad -= 5
            if self.grad == -255:
                all_sprites.append(Ball((randrange(15, 485), randrange(15, 485))))
                all_sprites.remove(self)

    def draw(self, surface):
        surface1 = surface.convert_alpha()
        surface1.fill([0, 0, 0, 0])
        color = pygame.Color((*self.color, 255 - abs(self.grad)))
        pygame.draw.circle(surface1, color, self.pos, 15)
        surface.blit(surface1, (0, 0))


def run():
    pygame.init()
    width, height = (500, 500)
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    all_sprites = []
    for i in range(10):
        ball = Ball((randrange(15, 485), randrange(15, 485)))
        all_sprites.append(ball)
    while True:
        key = pygame.key.get_pressed()
        buttons = []
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill('black')
        for ball in all_sprites:
            ball.update(all_sprites)
            ball.draw(screen)
        pygame.display.flip()
        # print(clock.get_fps())


if __name__ == "__main__":
    run()
    pygame.quit()
