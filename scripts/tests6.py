import pygame

from math import sin, cos, radians


class Blades:

    def __init__(self, pos, rot):
        self.x, self.y = pos
        self.rot = rot
        self.update(0)

    def update(self, rot):
        self.rot -= rot
        self.x1 = self.x - (sin(radians(self.rot - 15)) * 70)

        self.y1 = self.y - (cos(radians(self.rot - 15)) * 70)

        self.x2 = self.x - (sin(radians(self.rot + 15)) * 70)

        self.y2 = self.y - (cos(radians(self.rot + 15)) * 70)


    def draw(self, surface):
        pygame.draw.polygon(surface, 'white', ((self.x, self.y), (self.x1, self.y1), (self.x2, self.y2)))


def run():
    screen = pygame.display.set_mode((201, 201))

    pygame.display.set_caption('Вентилятор')

    blades = []

    blades.append(Blades((101, 101), 0))

    blades.append(Blades((101, 101), 120))

    blades.append(Blades((101, 101), 240))

    clock = pygame.time.Clock()

    rot = 0

    while True:

        screen.fill((0, 0, 0))

        clock.tick(100)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    rot += 5
                if event.button == 3:
                    rot -= 5

        for blad in blades:
            blad.update(rot)
            blad.draw(screen)

        pygame.draw.circle(screen, 'white', (101, 101), 10)

        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    run()

    pygame.quit()