import pygame
from characteristic import *
from math import fabs, sqrt
from threading import Thread


class Blinky(pygame.sprite.Sprite):
    def __init__(self, x, y, change_x, change_y):
        self.speed = 4.75
        self.past_way = ''
        pygame.sprite.Sprite.__init__(self)
        self.change_x = change_x
        self.change_y = change_y
        sheet = pygame.image.load("data/red animation.png")
        self.frames = []
        rows = 1
        columns = 4
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update_frame(self, scare=False):
        if self.past_way == 'way_right':
            self.image = self.frames[0]

        if self.past_way == 'way_down':
            self.image = self.frames[1]

        if self.past_way == 'way_left':
            self.image = self.frames[2]

        if self.past_way == 'way_up':
            self.image = self.frames[3]

        if scare:
            self.image = pygame.image.load('data/ghost-scared.png')

    def update(self, horizontal_blocks, vertical_blocks, player_x, player_y, change_x=0, change_y=0, red_x=0,
               red_y=0, scare_red=False, **kwargs):

        if scare_red:
            self.speed = 2.5
        else:
            self.speed = 4.80
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

        variable = [1, 16, 19, 20, 21, 29, 0, 23, 18]

        map = enviroment()
        if self.rect.topleft in self.get_intersection_position():
            way_up, way_down, way_right, way_left = sqrt(
                ((self.rect.x - player_x) ** 2) + ((self.rect.y - 25 - player_y) ** 2)), \
                                                    sqrt(((self.rect.x - player_x) ** 2) + (
                                                            (self.rect.y + 25 - player_y) ** 2)), \
                                                    sqrt(((self.rect.x + 25 - player_x) ** 2) + (
                                                            (self.rect.y - player_y) ** 2)), \
                                                    sqrt(((self.rect.x - 25 - player_x) ** 2) + (
                                                            (self.rect.y - player_y) ** 2))

            ways = [way_up, way_down, way_right, way_left]

            for i in range(len(ways) - 1):
                for j in range(len(ways) - i - 1):
                    if ways[j] > ways[j + 1]:
                        ways[j], ways[j + 1] = ways[j + 1], ways[j]

            for i in ways:
                if i == way_up and self.past_way != 'way_down' and map[round(self.rect.y / 25) - 1][
                    round(self.rect.x / 25)] in variable:
                    self.change_x = 0
                    self.change_y = -self.speed
                    self.past_way = 'way_up'
                    break
                elif i == way_right and self.past_way != 'way_left' and map[round(self.rect.y / 25)][
                    round(self.rect.x / 25) + 1] in variable:
                    self.change_x = self.speed
                    self.change_y = 0
                    self.past_way = 'way_right'
                    break
                elif i == way_left and self.past_way != 'way_right' and map[round(self.rect.y / 25)][
                    round(self.rect.x / 25) - 1] in variable:
                    self.change_x = -self.speed
                    self.change_y = 0
                    self.past_way = 'way_left'
                    break
                elif i == way_down and self.past_way != 'way_up' and map[round(self.rect.y / 25) + 1][
                    round(self.rect.x / 25)] in variable and map[round(self.rect.y / 25)][
                    round(self.rect.x / 25)] != 18:
                    self.change_x = 0
                    self.change_y = self.speed
                    self.past_way = 'way_down'
                    break
        elif self.rect.topleft == (225, 300):
            self.change_y = -1
            self.change_x = 0
        self.update_frame(scare=scare_red)

        try:
            if not map[round(self.rect.y / 25) - 1][round(self.rect.x / 25)] in variable and self.change_y < 0:
                if fabs(round(self.rect.y / 25) * 25 - self.rect.y) < 4:
                    self.rect.topleft = (self.rect.x, round(self.rect.y / 25) * 25)
                    self.change_y = 0

            elif not map[round(self.rect.y / 25) + 1][round(self.rect.x / 25)] in variable and self.change_y > 0:
                if fabs(round(self.rect.y / 25) * 25 - self.rect.y) < 4:
                    self.rect.topleft = (self.rect.x, round(self.rect.y / 25) * 25)
                    self.change_y = 0

            if not map[round(self.rect.y / 25)][round(self.rect.x / 25) - 1] in variable and self.change_x < 0:
                if fabs(round(self.rect.x / 25) * 25 - self.rect.x) < 4:
                    self.rect.topleft = (round(self.rect.x / 25) * 25, self.rect.y)
                    self.change_x = 0

            elif not map[round(self.rect.y / 25)][round(self.rect.x / 25) + 1] in variable and self.change_x > 0:
                if fabs(round(self.rect.x / 25) * 25 - self.rect.x) < 4:
                    self.rect.topleft = (round(self.rect.x / 25) * 25, self.rect.y)
                    self.change_x = 0
        except IndexError:
            if self.change_x < 0:
                self.change_x = -2
            else:
                self.change_x = 2

    def get_intersection_position(self):
        items = []
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item == 19 or item == 23 or item == 18:
                    items.append((j * 25, i * 25))

        return items


class Pinky(pygame.sprite.Sprite):
    def __init__(self, x, y, change_x, change_y):
        self.speed = 4
        self.past_way = ''
        pygame.sprite.Sprite.__init__(self)
        self.change_x = change_x
        self.change_y = change_y
        sheet = pygame.image.load("data/pink animation.png")
        self.frames = []
        rows = 1
        columns = 4
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update_frame(self, scare):
        if self.past_way == 'way_right':
            self.image = self.frames[0]

        if self.past_way == 'way_down':
            self.image = self.frames[1]

        if self.past_way == 'way_left':
            self.image = self.frames[2]

        if self.past_way == 'way_up':
            self.image = self.frames[3]

        if scare:
            self.image = pygame.image.load('data/ghost-scared.png')

    def update(self, horizontal_blocks, vertical_blocks, player_x, player_y, change_x=0, change_y=0, red_x=0,
               red_y=0, scare_pink=False, **kwargs):

        if scare_pink:
            self.speed = 2.5
        else:
            self.speed = 4.60
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

        variable = [1, 16, 19, 20, 21, 0, 18, 29, 23]

        map = enviroment()
        if self.rect.topleft in self.get_intersection_position():
            if change_x > 0:
                way_up, way_down, way_right, way_left = sqrt(
                    ((self.rect.x - player_x + 100) ** 2) + ((self.rect.y - 25 - player_y) ** 2)), \
                                                        sqrt(((self.rect.x - player_x + 100) ** 2) + (
                                                                (self.rect.y + 25 - player_y) ** 2)), \
                                                        sqrt(((self.rect.x + 125 - player_x) ** 2) + (
                                                                (self.rect.y - player_y) ** 2)), \
                                                        sqrt(((self.rect.x + 75 - player_x) ** 2) + (
                                                                (self.rect.y - player_y) ** 2))
            if change_x < 0:
                way_up, way_down, way_right, way_left = sqrt(
                    ((self.rect.x - player_x - 100) ** 2) + ((self.rect.y - 25 - player_y) ** 2)), \
                                                        sqrt(((self.rect.x - player_x - 100) ** 2) + (
                                                                (self.rect.y + 25 - player_y) ** 2)), \
                                                        sqrt(((self.rect.x - 75 - player_x) ** 2) + (
                                                                (self.rect.y - player_y) ** 2)), \
                                                        sqrt(((self.rect.x - 125 - player_x) ** 2) + (
                                                                (self.rect.y - player_y) ** 2))

            elif change_y > 0:
                way_up, way_down, way_right, way_left = sqrt(
                    ((self.rect.x - player_x) ** 2) + ((self.rect.y + 75 - player_y) ** 2)), \
                                                        sqrt(((self.rect.x - player_x) ** 2) + (
                                                                (self.rect.y + 125 - player_y) ** 2)), \
                                                        sqrt(((self.rect.x + 25 - player_x) ** 2) + (
                                                                (self.rect.y - player_y + 100) ** 2)), \
                                                        sqrt(((self.rect.x - 25 - player_x) ** 2) + (
                                                                (self.rect.y - player_y + 100) ** 2))
            elif change_y < 0:
                way_up, way_down, way_right, way_left = sqrt(
                    ((self.rect.x - player_x) ** 2) + ((self.rect.y - 125 - player_y) ** 2)), \
                                                        sqrt(((self.rect.x - player_x) ** 2) + (
                                                                (self.rect.y - 75 - player_y) ** 2)), \
                                                        sqrt(((self.rect.x + 25 - player_x) ** 2) + (
                                                                (self.rect.y - player_y - 100) ** 2)), \
                                                        sqrt(((self.rect.x - 25 - player_x) ** 2) + (
                                                                (self.rect.y - player_y - 100) ** 2))
            else:
                way_up, way_down, way_right, way_left = sqrt(
                    ((self.rect.x - player_x) ** 2) + ((self.rect.y - 25 - player_y) ** 2)), \
                                                        sqrt(((self.rect.x - player_x) ** 2) + (
                                                                (self.rect.y + 25 - player_y) ** 2)), \
                                                        sqrt(((self.rect.x + 25 - player_x) ** 2) + (
                                                                (self.rect.y - player_y) ** 2)), \
                                                        sqrt(((self.rect.x - 25 - player_x) ** 2) + (
                                                                (self.rect.y - player_y) ** 2))

            ways = [way_up, way_down, way_right, way_left]

            for i in range(len(ways) - 1):
                for j in range(len(ways) - i - 1):
                    if ways[j] > ways[j + 1]:
                        ways[j], ways[j + 1] = ways[j + 1], ways[j]

            for i in ways:
                if i == way_up and self.past_way != 'way_down' and map[round(self.rect.y / 25) - 1][
                    round(self.rect.x / 25)] in variable:
                    self.change_x = 0
                    self.change_y = -self.speed
                    self.past_way = 'way_up'
                    break
                elif i == way_right and self.past_way != 'way_left' and map[round(self.rect.y / 25)][
                    round(self.rect.x / 25) + 1] in variable:
                    self.change_x = self.speed
                    self.change_y = 0
                    self.past_way = 'way_right'
                    break
                elif i == way_left and self.past_way != 'way_right' and map[round(self.rect.y / 25)][
                    round(self.rect.x / 25) - 1] in variable:
                    self.change_x = -self.speed
                    self.change_y = 0
                    self.past_way = 'way_left'
                    break
                elif i == way_down and self.past_way != 'way_up' and map[round(self.rect.y / 25) + 1][
                    round(self.rect.x / 25)] in variable and map[round(self.rect.y / 25)][
                    round(self.rect.x / 25)] != 18:
                    self.change_x = 0
                    self.change_y = self.speed
                    self.past_way = 'way_down'
                    break
        elif self.rect.topleft == (225, 300):
            self.change_y = -1
            change_x = 0

        self.update_frame(scare=scare_pink)

        try:
            if not map[round(self.rect.y / 25) - 1][round(self.rect.x / 25)] in variable and self.change_y < 0:
                if fabs(round(self.rect.y / 25) * 25 - self.rect.y) < 4:
                    self.rect.topleft = (self.rect.x, round(self.rect.y / 25) * 25)
                    self.change_y = 0

            elif not map[round(self.rect.y / 25) + 1][round(self.rect.x / 25)] in variable and self.change_y > 0:
                if fabs(round(self.rect.y / 25) * 25 - self.rect.y) < 4:
                    self.rect.topleft = (self.rect.x, round(self.rect.y / 25) * 25)
                    self.change_y = 0

            if not map[round(self.rect.y / 25)][round(self.rect.x / 25) - 1] in variable and self.change_x < 0:
                if fabs(round(self.rect.x / 25) * 25 - self.rect.x) < 4:
                    self.rect.topleft = (round(self.rect.x / 25) * 25, self.rect.y)
                    self.change_x = 0

            elif not map[round(self.rect.y / 25)][round(self.rect.x / 25) + 1] in variable and self.change_x > 0:
                if fabs(round(self.rect.x / 25) * 25 - self.rect.x) < 4:
                    self.rect.topleft = (round(self.rect.x / 25) * 25, self.rect.y)
                    self.change_x = 0
        except IndexError:
            if self.change_x < 0:
                self.change_x = -2
            else:
                self.change_x = 2

    def get_intersection_position(self):
        items = []
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item == 19 or item == 18 or item == 23:
                    items.append((j * 25, i * 25))

        return items


class Inky(pygame.sprite.Sprite):
    def __init__(self, x, y, change_x, change_y):
        self.speed = 4.75
        self.past_way = ''
        pygame.sprite.Sprite.__init__(self)
        self.change_x = change_x
        self.change_y = change_y
        sheet = pygame.image.load("data/blue animation.png")
        self.frames = []
        rows = 1
        columns = 4
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update_frame(self, scare):
        if self.past_way == 'way_right':
            self.image = self.frames[0]

        if self.past_way == 'way_down':
            self.image = self.frames[1]

        if self.past_way == 'way_left':
            self.image = self.frames[2]

        if self.past_way == 'way_up':
            self.image = self.frames[3]

        if scare:
            self.image = pygame.image.load('data/ghost-scared.png')

    def update(self, horizontal_blocks, vertical_blocks, player_x, player_y, change_x=0, change_y=0, red_x=0,
               red_y=0, scare_blue=False, **kwargs):

        if scare_blue:
            self.speed = 2.5
        else:
            self.speed = 4.7
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

        variable = [1, 16, 19, 20, 21, 0, 29, 18, 23]
        map = enviroment()
        if self.rect.topleft in self.get_intersection_position():
            way = self.my_way(red_x, red_y, player_x, player_y, change_x, change_y)

            way_up, way_down, way_right, way_left = sqrt(
                ((self.rect.x - way[0]) ** 2) + ((self.rect.y - 25 - way[1]) ** 2)) * 2, \
                                                    sqrt(((self.rect.x - way[0]) ** 2) + (
                                                            (self.rect.y + 25 - way[1]) ** 2)) * 2, \
                                                    sqrt(((self.rect.x + 25 - way[0]) ** 2) + (
                                                            (self.rect.y - way[1]) ** 2)) * 2, \
                                                    sqrt(((self.rect.x - 25 - way[0]) ** 2) + (
                                                            (self.rect.y - way[1]) ** 2)) * 2
            ways = [way_up, way_down, way_right, way_left]

            for i in range(len(ways) - 1):
                for j in range(len(ways) - i - 1):
                    if ways[j] > ways[j + 1]:
                        ways[j], ways[j + 1] = ways[j + 1], ways[j]
            for i in ways:
                if i == way_up and self.past_way != 'way_down' and map[round(self.rect.y / 25) - 1][
                    round(self.rect.x / 25)] in variable:
                    self.change_x = 0
                    self.change_y = -self.speed
                    self.past_way = 'way_up'
                    break
                elif i == way_right and self.past_way != 'way_left' and map[round(self.rect.y / 25)][
                    round(self.rect.x / 25) + 1] in variable:
                    self.change_x = self.speed
                    self.change_y = 0
                    self.past_way = 'way_right'
                    break
                elif i == way_left and self.past_way != 'way_right' and map[round(self.rect.y / 25)][
                    round(self.rect.x / 25) - 1] in variable:
                    self.change_x = -self.speed
                    self.change_y = 0
                    self.past_way = 'way_left'
                    break
                elif i == way_down and self.past_way != 'way_up' and map[round(self.rect.y / 25) + 1][
                    round(self.rect.x / 25)] in variable and map[round(self.rect.y / 25)][
                    round(self.rect.x / 25)] != 18:
                    self.change_x = 0
                    self.change_y = self.speed
                    self.past_way = 'way_down'
                    break
        elif self.rect.topleft == (225, 300):
            self.change_y = -1
            self.change_x = 0
        elif self.rect.topleft == (10 * 25, 12 * 25):
            self.change_x = -1
            self.change_y = 0
        self.update_frame(scare=scare_blue)

        try:
            if not map[round(self.rect.y / 25) - 1][round(self.rect.x / 25)] in variable and self.change_y < 0:
                if fabs(round(self.rect.y / 25) * 25 - self.rect.y) < 4:
                    self.rect.topleft = (self.rect.x, round(self.rect.y / 25) * 25)
                    self.change_y = 0

            elif not map[round(self.rect.y / 25) + 1][round(self.rect.x / 25)] in variable and self.change_y > 0:
                if fabs(round(self.rect.y / 25) * 25 - self.rect.y) < 4:
                    self.rect.topleft = (self.rect.x, round(self.rect.y / 25) * 25)
                    self.change_y = 0

            if not map[round(self.rect.y / 25)][round(self.rect.x / 25) - 1] in variable and self.change_x < 0:
                if fabs(round(self.rect.x / 25) * 25 - self.rect.x) < 4:
                    self.rect.topleft = (round(self.rect.x / 25) * 25, self.rect.y)
                    self.change_x = 0

            elif not map[round(self.rect.y / 25)][round(self.rect.x / 25) + 1] in variable and self.change_x > 0:
                if fabs(round(self.rect.x / 25) * 25 - self.rect.x) < 4:
                    self.rect.topleft = (round(self.rect.x / 25) * 25, self.rect.y)
                    self.change_x = 0
        except IndexError:
            if self.change_x < 0:
                self.change_x = -2
            else:
                self.change_x = 2

    def get_intersection_position(self):
        items = []
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item == 19 or item == 18 or item == 23:
                    items.append((j * 25, i * 25))

        return items

    def my_way(self, red_x: int, red_y: int, player_x: int, player_y: int, change_x: int, change_y: int) -> tuple:

        point = ()
        if change_x > 0:
            player_x += 50
            point = (player_x * 2 - red_x, player_y * 2 - red_y)
        elif change_x < 0:
            player_x -= 50
            point = (player_x * 2 - red_x, player_y * 2 - red_y)
        elif change_y > 0:
            player_y += 50
            point = (player_x * 2 - red_x, player_y * 2 - red_y)
        elif change_y < 0:
            player_y -= 50
            point = (player_x * 2 - red_x, player_y * 2 - red_y)
        else:
            player_x += 50
            point = (player_x * 2 - red_x, player_y * 2 - red_y)

        return point
        # way_up, way_down, way_right, way_left = sqrt(
        #     ((red_x - player_x) ** 2) + ((red_y - 25 - player_y) ** 2)), \
        #                                         sqrt(((red_x - player_x) ** 2) + (
        #                                                 (red_y + 25 - player_y) ** 2)), \
        #                                         sqrt(((red_x + 25 - player_x) ** 2) + (
        #                                                 (red_y - player_y) ** 2)), \
        #                                         sqrt(((red_x - 25 - player_x) ** 2) + (
        #                                                 (red_y - player_y) ** 2))


class Clyde(pygame.sprite.Sprite):
    def __init__(self, x, y, change_x, change_y):
        self.speed = 4.75
        self.past_way = ''
        pygame.sprite.Sprite.__init__(self)
        self.change_x = change_x
        self.change_y = change_y
        sheet = pygame.image.load("data/orange animation.png")
        self.frames = []
        rows = 1
        columns = 4
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update_frame(self, scare=False):
        if self.past_way == 'way_right':
            self.image = self.frames[0]

        if self.past_way == 'way_down':
            self.image = self.frames[1]

        if self.past_way == 'way_left':
            self.image = self.frames[2]

        if self.past_way == 'way_up':
            self.image = self.frames[3]

        if scare:
            self.image = pygame.image.load('data/ghost-scared.png')

    def update(self, horizontal_blocks, vertical_blocks, player_x, player_y, change_x=0, change_y=0, red_x=0,
               red_y=0, scare_orange=False, **kwargs):
        if scare_orange:
            self.speed = 2.5
        else:
            self.speed = 4.4

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

        variable = [1, 16, 19, 20, 21, 29, 0, 23, 18]

        map = enviroment()
        if self.rect.topleft in self.get_intersection_position():
            way_up, way_down, way_right, way_left = sqrt(
                ((self.rect.x - player_x) ** 2) + ((self.rect.y - 25 - player_y) ** 2)), \
                                                    sqrt(((self.rect.x - player_x) ** 2) + (
                                                            (self.rect.y + 25 - player_y) ** 2)), \
                                                    sqrt(((self.rect.x + 25 - player_x) ** 2) + (
                                                            (self.rect.y - player_y) ** 2)), \
                                                    sqrt(((self.rect.x - 25 - player_x) ** 2) + (
                                                            (self.rect.y - player_y) ** 2))

            ways = [i for i in [way_up, way_left, way_right, way_down] if i <= 800]
            if not ways:
                ways = [way_up, way_down, way_right, way_left]

            for i in range(len(ways) - 1):
                for j in range(len(ways) - i - 1):
                    if ways[j] > ways[j + 1]:
                        ways[j], ways[j + 1] = ways[j + 1], ways[j]

            for i in ways:
                if i == way_up and self.past_way != 'way_down' and map[round(self.rect.y / 25) - 1][
                    round(self.rect.x / 25)] in variable:
                    self.change_x = 0
                    self.change_y = -self.speed
                    self.past_way = 'way_up'
                    break
                elif i == way_right and self.past_way != 'way_left' and map[round(self.rect.y / 25)][
                    round(self.rect.x / 25) + 1] in variable:
                    self.change_x = self.speed
                    self.change_y = 0
                    self.past_way = 'way_right'
                    break
                elif i == way_left and self.past_way != 'way_right' and map[round(self.rect.y / 25)][
                    round(self.rect.x / 25) - 1] in variable:
                    self.change_x = -self.speed
                    self.change_y = 0
                    self.past_way = 'way_left'
                    break
                elif i == way_down and self.past_way != 'way_up' and map[round(self.rect.y / 25) + 1][
                    round(self.rect.x / 25)] in variable and map[round(self.rect.y / 25)][
                    round(self.rect.x / 25)] != 18:
                    self.change_x = 0
                    self.change_y = self.speed
                    self.past_way = 'way_down'
                    break
        elif self.rect.topleft == (225, 300):
            self.change_y = -1
            self.change_x = 0
        elif self.rect.topleft == (8 * 25, 12 * 25):
            self.change_x = 1
            self.change_y = 0
        self.update_frame(scare=scare_orange)

        try:
            if not map[round(self.rect.y / 25) - 1][round(self.rect.x / 25)] in variable and self.change_y < 0:
                if fabs(round(self.rect.y / 25) * 25 - self.rect.y) < 4:
                    self.rect.topleft = (self.rect.x, round(self.rect.y / 25) * 25)
                    self.change_y = 0

            elif not map[round(self.rect.y / 25) + 1][round(self.rect.x / 25)] in variable and self.change_y > 0:
                if fabs(round(self.rect.y / 25) * 25 - self.rect.y) < 4:
                    self.rect.topleft = (self.rect.x, round(self.rect.y / 25) * 25)
                    self.change_y = 0

            if not map[round(self.rect.y / 25)][round(self.rect.x / 25) - 1] in variable and self.change_x < 0:
                if fabs(round(self.rect.x / 25) * 25 - self.rect.x) < 4:
                    self.rect.topleft = (round(self.rect.x / 25) * 25, self.rect.y)
                    self.change_x = 0

            elif not map[round(self.rect.y / 25)][round(self.rect.x / 25) + 1] in variable and self.change_x > 0:
                if fabs(round(self.rect.x / 25) * 25 - self.rect.x) < 4:
                    self.rect.topleft = (round(self.rect.x / 25) * 25, self.rect.y)
                    self.change_x = 0
        except IndexError:
            if self.change_x < 0:
                self.change_x = -2
            else:
                self.change_x = 2

    def get_intersection_position(self):
        items = []
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item == 19 or item == 23 or item == 18:
                    items.append((j * 25, i * 25))

        return items


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


class Berry(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/berry.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


def enviroment():
    field = tuple([tuple(map(int, i.strip().split())) for i in open('data/map.txt', mode='r').readlines()])
    # field = ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    #  (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    #  (2, 10, 10, 10, 10, 10, 10, 10, 10, 12, 10, 10, 10, 10, 10, 10, 10, 10, 3),
    #  (11, 19, 1, 1, 19, 1, 1, 1, 19, 11, 19, 1, 1, 1, 19, 1, 1, 19, 11),
    #  (11, 16, 2, 3, 16, 2, 12, 3, 16, 11, 16, 2, 12, 3, 16, 2, 3, 16, 11),
    #  (11, 16, 4, 5, 16, 4, 13, 5, 16, 9, 16, 4, 13, 5, 16, 4, 5, 16, 11),
    #  (11, 19, 1, 1, 19, 1, 19, 1, 19, 1, 19, 1, 19, 1, 19, 1, 1, 19, 11),
    #  (11, 16, 6, 7, 16, 8, 16, 6, 10, 12, 10, 7, 16, 8, 16, 6, 7, 16, 11),
    #  (11, 19, 1, 1, 19, 11, 19, 1, 19, 11, 19, 1, 19, 11, 19, 1, 1, 19, 11),
    #  (4, 10, 10, 3, 16, 14, 10, 7, 16, 9, 16, 6, 10, 15, 16, 2, 10, 10, 5),
    #  (0, 0, 0, 11, 16, 11, 19, 1, 19, 1, 19, 1, 19, 11, 16, 11, 0, 0, 0),
    #  (10, 10, 10, 5, 16, 9, 16, 2, 12, 12, 12, 3, 16, 9, 16, 4, 10, 10, 10),
    #  (1, 1, 1, 1, 19, 1, 19, 14, 0, 0, 0, 15, 19, 1, 19, 1, 1, 1, 1),
    #  (10, 10, 10, 3, 16, 8, 16, 4, 13, 13, 13, 5, 16, 8, 16, 2, 10, 10, 10),
    #  (0, 0, 0, 11, 16, 11, 19, 1, 1, 1, 1, 1, 19, 11, 16, 11, 0, 0, 0),
    #  (2, 10, 10, 5, 16, 9, 16, 6, 10, 12, 10, 7, 16, 9, 16, 4, 10, 10, 3),
    #  (11, 19, 1, 1, 19, 1, 19, 1, 19, 11, 19, 1, 19, 1, 19, 1, 1, 19, 11),
    #  (11, 16, 6, 3, 16, 6, 10, 7, 16, 9, 16, 6, 10, 7, 16, 2, 7, 16, 11),
    #  (11, 19, 19, 11, 19, 1, 19, 1, 19, 20, 19, 1, 19, 1, 19, 11, 19, 19, 11),
    #  (14, 7, 16, 9, 16, 8, 16, 6, 10, 12, 10, 7, 16, 8, 16, 9, 16, 6, 15),
    #  (11, 19, 19, 1, 19, 11, 19, 1, 19, 11, 19, 1, 19, 11, 19, 1, 19, 19, 11),
    #  (11, 16, 6, 10, 10, 13, 10, 7, 16, 9, 16, 6, 10, 13, 10, 10, 7, 16, 11),
    #  (11, 19, 1, 1, 1, 1, 1, 1, 19, 1, 19, 1, 1, 1, 1, 1, 1, 19, 11),
    #  (4, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 5))

    return field


def draw_enviroment(screen):
    size = 25
    for i, row in enumerate(enviroment()):
        for j, item in enumerate(row):
            if item == 2:
                pygame.draw.line(screen, BLUE, [j * size, i * size], [j * size + size, i * size], 2)
                pygame.draw.line(screen, BLUE, [j * size, i * size], [j * size, i * size + size], 2)
            elif item == 3:
                pygame.draw.line(screen, BLUE, [j * size, i * size], [j * size + size, i * size], 2)
                pygame.draw.line(screen, BLUE, [j * size + size, i * size], [j * size + size, i * size + size], 2)
            elif item == 4:
                pygame.draw.line(screen, BLUE, [j * size, i * size], [j * size, i * size + size], 2)
                pygame.draw.line(screen, BLUE, [j * size, i * size + size], [j * size + size, i * size + size], 2)
            elif item == 5:
                pygame.draw.line(screen, BLUE, [j * size + size, i * size], [j * size + size, i * size + size], 2)
                pygame.draw.line(screen, BLUE, [j * size, i * size + size], [j * size + size, i * size + size], 2)
            elif item == 6:
                pygame.draw.line(screen, BLUE, [j * size, i * size], [j * size + size, i * size], 2)
                pygame.draw.line(screen, BLUE, [j * size, i * size], [j * size, i * size + size], 2)
                pygame.draw.line(screen, BLUE, [j * size, i * size + size], [j * size + size, i * size + size], 2)
            elif item == 7:
                pygame.draw.line(screen, BLUE, [j * size, i * size], [j * size + size, i * size], 2)
                pygame.draw.line(screen, BLUE, [j * size + size, i * size], [j * size + size, i * size + size], 2)
                pygame.draw.line(screen, BLUE, [j * size, i * size + size], [j * size + size, i * size + size], 2)
            elif item == 8:
                pygame.draw.line(screen, BLUE, [j * size, i * size], [j * size + size, i * size], 2)
                pygame.draw.line(screen, BLUE, [j * size, i * size], [j * size, i * size + size], 2)
                pygame.draw.line(screen, BLUE, [j * size + size, i * size], [j * size + size, i * size + size], 2)
            elif item == 9:
                pygame.draw.line(screen, BLUE, [j * size + size, i * size], [j * size + size, i * size + size], 2)
                pygame.draw.line(screen, BLUE, [j * size, i * size], [j * size, i * size + size], 2)
                pygame.draw.line(screen, BLUE, [j * size, i * size + size], [j * size + size, i * size + size], 2)
            elif item == 10:
                pygame.draw.line(screen, BLUE, [j * size, i * size], [j * size + size, i * size], 2)
                pygame.draw.line(screen, BLUE, [j * size, i * size + size], [j * size + size, i * size + size], 2)
            elif item == 11:
                pygame.draw.line(screen, BLUE, [j * size, i * size], [j * size, i * size + size], 2)
                pygame.draw.line(screen, BLUE, [j * size + size, i * size], [j * size + size, i * size + size], 2)
            elif item == 12:
                pygame.draw.line(screen, BLUE, [j * size, i * size], [j * size + size, i * size], 2)
            elif item == 13:
                pygame.draw.line(screen, BLUE, [j * size, i * size + size], [j * size + size, i * size + size], 2)
            elif item == 14:
                pygame.draw.line(screen, BLUE, [j * size, i * size], [j * size, i * size + size], 2)
            elif item == 15:
                pygame.draw.line(screen, BLUE, [j * size + size, i * size], [j * size + size, i * size + size], 2)
