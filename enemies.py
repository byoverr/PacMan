import pygame
import random

SCREEN_WIDTH = 475
SCREEN_HEIGHT = 625

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Ellipse(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y, change_x, change_y):
        pygame.sprite.Sprite.__init__(self)
        self.change_x = change_x
        self.change_y = change_y
        self.image = pygame.image.load("slime.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, horizontal_blocks, vertical_blocks):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0

        if self.rect.topleft in self.get_intersection_position():
            direction = random.choice(("left", "right", "up", "down"))
            if direction == "left" and self.change_x == 0:
                self.change_x = -2
                self.change_y = 0
            elif direction == "right" and self.change_x == 0:
                self.change_x = 2
                self.change_y = 0
            elif direction == "up" and self.change_y == 0:
                self.change_x = 0
                self.change_y = -2
            elif direction == "down" and self.change_y == 0:
                self.change_x = 0
                self.change_y = 2

    def get_intersection_position(self):
        items = []
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item == 19:
                    items.append((j * 25, i * 25))

        return items


def enviroment():
    grid = ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            (2, 10, 10, 10, 10, 10, 10, 10, 10, 12, 10, 10, 10, 10, 10, 10, 10, 10, 3),
            (11, 19, 1, 1, 19, 1, 1, 1, 19, 11, 19, 1, 1, 1, 19, 1, 1, 19, 11),
            (11, 16, 2, 3, 16, 2, 12, 3, 16, 11, 16, 2, 12, 3, 16, 2, 3, 16, 11),
            (11, 16, 4, 5, 16, 4, 13, 5, 16, 9, 16, 4, 13, 5, 16, 4, 5, 16, 11),
            (11, 19, 1, 1, 19, 1, 19, 1, 19, 1, 19, 1, 19, 1, 19, 1, 1, 19, 11),
            (11, 16, 6, 7, 16, 8, 16, 6, 10, 12, 10, 7, 16, 8, 16, 6, 7, 16, 11),
            (11, 19, 1, 1, 19, 11, 19, 1, 19, 11, 19, 1, 19, 11, 19, 1, 1, 19, 11),
            (4, 10, 10, 3, 16, 14, 10, 7, 16, 9, 16, 6, 10, 15, 16, 2, 10, 10, 5),
            (0, 0, 0, 11, 16, 11, 19, 1, 19, 1, 19, 1, 19, 11, 16, 11, 0, 0, 0),
            (10, 10, 10, 5, 16, 9, 16, 2, 12, 12, 12, 3, 16, 9, 16, 4, 10, 10, 10),
            (1, 1, 1, 1, 19, 1, 19, 14, 0, 0, 0, 15, 19, 1, 19, 1, 1, 1, 1),
            (10, 10, 10, 3, 16, 8, 16, 4, 13, 13, 13, 5, 16, 8, 16, 2, 10, 10, 10),
            (0, 0, 0, 11, 16, 11, 19, 1, 1, 1, 1, 1, 19, 11, 16, 11, 0, 0, 0),
            (2, 10, 10, 5, 16, 9, 16, 6, 10, 12, 10, 7, 16, 9, 16, 4, 10, 10, 3),
            (11, 19, 1, 1, 19, 1, 19, 1, 19, 11, 19, 1, 19, 1, 19, 1, 1, 19, 11),
            (11, 16, 6, 3, 16, 6, 10, 7, 16, 9, 16, 6, 10, 7, 16, 2, 7, 16, 11),
            (11, 19, 19, 11, 19, 1, 19, 1, 19, 20, 19, 1, 19, 1, 19, 11, 19, 19, 11),
            (14, 7, 16, 9, 16, 8, 16, 6, 10, 12, 10, 7, 16, 8, 16, 9, 16, 6, 15),
            (11, 19, 19, 1, 19, 11, 19, 1, 19, 11, 19, 1, 19, 11, 19, 1, 19, 19, 11),
            (11, 16, 6, 10, 10, 13, 10, 7, 16, 9, 16, 6, 10, 13, 10, 10, 7, 16, 11),
            (11, 19, 1, 1, 1, 1, 1, 1, 19, 1, 19, 1, 1, 1, 1, 1, 1, 19, 11),
            (4, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 5))

    return grid


def draw_enviroment(screen):
    for i, row in enumerate(enviroment()):
        for j, item in enumerate(row):
            if item == 2:
                pygame.draw.line(screen, BLUE, [j * 25, i * 25], [j * 25 + 25, i * 25], 2)
                pygame.draw.line(screen, BLUE, [j * 25, i * 25], [j * 25, i * 25 + 25], 2)
            elif item == 3:
                pygame.draw.line(screen, BLUE, [j * 25, i * 25], [j * 25 + 25, i * 25], 2)
                pygame.draw.line(screen, BLUE, [j * 25 + 25, i * 25], [j * 25 + 25, i * 25 + 25], 2)
            elif item == 4:
                pygame.draw.line(screen, BLUE, [j * 25, i * 25], [j * 25, i * 25 + 25], 2)
                pygame.draw.line(screen, BLUE, [j * 25, i * 25 + 25], [j * 25 + 25, i * 25 + 25], 2)
            elif item == 5:
                pygame.draw.line(screen, BLUE, [j * 25 + 25, i * 25], [j * 25 + 25, i * 25 + 25], 2)
                pygame.draw.line(screen, BLUE, [j * 25, i * 25 + 25], [j * 25 + 25, i * 25 + 25], 2)
            elif item == 6:
                pygame.draw.line(screen, BLUE, [j * 25, i * 25], [j * 25 + 25, i * 25], 2)
                pygame.draw.line(screen, BLUE, [j * 25, i * 25], [j * 25, i * 25 + 25], 2)
                pygame.draw.line(screen, BLUE, [j * 25, i * 25 + 25], [j * 25 + 25, i * 25 + 25], 2)
            elif item == 7:
                pygame.draw.line(screen, BLUE, [j * 25, i * 25], [j * 25 + 25, i * 25], 2)
                pygame.draw.line(screen, BLUE, [j * 25 + 25, i * 25], [j * 25 + 25, i * 25 + 25], 2)
                pygame.draw.line(screen, BLUE, [j * 25, i * 25 + 25], [j * 25 + 25, i * 25 + 25], 2)
            elif item == 8:
                pygame.draw.line(screen, BLUE, [j * 25, i * 25], [j * 25 + 25, i * 25], 2)
                pygame.draw.line(screen, BLUE, [j * 25, i * 25], [j * 25, i * 25 + 25], 2)
                pygame.draw.line(screen, BLUE, [j * 25 + 25, i * 25], [j * 25 + 25, i * 25 + 25], 2)
            elif item == 9:
                pygame.draw.line(screen, BLUE, [j * 25 + 25, i * 25], [j * 25 + 25, i * 25 + 25], 2)
                pygame.draw.line(screen, BLUE, [j * 25, i * 25], [j * 25, i * 25 + 25], 2)
                pygame.draw.line(screen, BLUE, [j * 25, i * 25 + 25], [j * 25 + 25, i * 25 + 25], 2)
            elif item == 10:
                pygame.draw.line(screen, BLUE, [j * 25, i * 25], [j * 25 + 25, i * 25], 2)
                pygame.draw.line(screen, BLUE, [j * 25, i * 25 + 25], [j * 25 + 25, i * 25 + 25], 2)
            elif item == 11:
                pygame.draw.line(screen, BLUE, [j * 25, i * 25], [j * 25, i * 25 + 25], 2)
                pygame.draw.line(screen, BLUE, [j * 25 + 25, i * 25], [j * 25 + 25, i * 25 + 25], 2)
            elif item == 12:
                pygame.draw.line(screen, BLUE, [j * 25, i * 25], [j * 25 + 25, i * 25], 2)
            elif item == 13:
                pygame.draw.line(screen, BLUE, [j * 25, i * 25 + 25], [j * 25 + 25, i * 25 + 25], 2)
            elif item == 14:
                pygame.draw.line(screen, BLUE, [j * 25, i * 25], [j * 25, i * 25 + 25], 2)
            elif item == 15:
                pygame.draw.line(screen, BLUE, [j * 25 + 25, i * 25], [j * 25 + 25, i * 25 + 25], 2)
