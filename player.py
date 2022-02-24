import pygame
from characteristic import *
from math import fabs
from enemies import enviroment


class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    explosion = False
    round_over = False
    speed = 5

    def __init__(self, x, y, filename):
        self.future_left = False
        self.future_down = False
        self.future_right = False
        self.future_up = False
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        img = pygame.image.load("data/walk.png").convert()
        # создание анимации
        self.move_right_animation = Animation(img, 25, 25)
        self.move_left_animation = Animation(pygame.transform.flip(img, True, False), 25, 25)
        self.move_up_animation = Animation(pygame.transform.rotate(img, 90), 25, 25)
        self.move_down_animation = Animation(pygame.transform.rotate(img, 270), 25, 25)
        # загрузка взрыва пакмана
        img = pygame.image.load("data/explosion.png").convert()
        self.explosion_animation = Animation(img, 25, 25)
        self.player_image = pygame.image.load(filename).convert()
        self.player_image.set_colorkey(BLACK)

    def update(self, horizontal_blocks, vertical_blocks):
        variable = [1, 16, 19, 20, 21, 18, 23]

        map = enviroment()

        # идеальное передвижение PacMan
        try:
            if map[round(self.rect.y / 25) - 1][round(self.rect.x / 25)] in variable and self.future_up:
                if not self.future_down:
                    if fabs(round(self.rect.x / 25) * 25 - self.rect.x) < 2:
                        self.rect.topleft = (round(self.rect.x / 25) * 25, self.rect.y)
                        self.change_y = -self.speed
                        self.change_x = 0
                        self.future_down = False
                        self.future_up = False
                        self.future_right = False
                        self.future_left = False
                        self.future_right = False
                else:
                    self.change_y = self.speed
                    self.future_down = False
                    self.future_up = False
                    self.future_right = False
                    self.future_left = False
                    self.future_right = False

            elif map[round(self.rect.y / 25) + 1][round(self.rect.x / 25)] in variable and self.future_down:
                if not self.future_up:
                    if fabs(round(self.rect.x / 25) * 25 - self.rect.x) < 2:
                        self.rect.topleft = (round(self.rect.x / 25) * 25, self.rect.y)
                        self.change_y = self.speed
                        self.change_x = 0
                        self.future_down = False
                        self.future_up = False
                        self.future_right = False
                        self.future_left = False
                        self.future_right = False
                else:
                    self.change_y = self.speed
                    self.future_down = False
                    self.future_up = False
                    self.future_right = False
                    self.future_left = False
                    self.future_right = False

            if map[round(self.rect.y / 25)][round(self.rect.x / 25) - 1] in variable and self.future_left:
                if not self.future_right:
                    if fabs(round(self.rect.y / 25) * 25 - self.rect.y) < 2:
                        self.rect.topleft = (self.rect.x, round(self.rect.y / 25) * 25)
                        self.change_y = 0
                        self.change_x = -self.speed
                        self.future_down = False
                        self.future_up = False
                        self.future_right = False
                        self.future_left = False
                        self.future_right = False
                else:
                    self.change_x = -self.speed
                    self.future_down = False
                    self.future_up = False
                    self.future_right = False
                    self.future_left = False
                    self.future_right = False

            elif map[round(self.rect.y / 25)][round(self.rect.x / 25) + 1] in variable and self.future_right:
                if not self.future_left:
                    if fabs(round(self.rect.y / 25) * 25 - self.rect.y) < 2:
                        self.rect.topleft = (self.rect.x, round(self.rect.y / 25) * 25)
                        self.change_y = 0
                        self.change_x = self.speed
                        self.future_down = False
                        self.future_up = False
                        self.future_right = False
                        self.future_left = False
                        self.future_right = False
                else:
                    self.change_x = self.speed
                    self.future_down = False
                    self.future_up = False
                    self.future_right = False
                    self.future_left = False
                    self.future_right = False
        except IndexError:
            pass

        # остановка пакмена перед стеной
        try:
            if not map[round(self.rect.y / 25) - 1][round(self.rect.x / 25)] in variable and self.change_y < 0:
                if fabs(round(self.rect.y / 25) * 25 - self.rect.y) < 2:
                    self.rect.topleft = (self.rect.x, round(self.rect.y / 25) * 25)
                    self.change_y = 0

            elif not map[round(self.rect.y / 25) + 1][round(self.rect.x / 25)] in variable and self.change_y > 0:
                if fabs(round(self.rect.y / 25) * 25 - self.rect.y) < 2:
                    self.rect.topleft = (self.rect.x, round(self.rect.y / 25) * 25)
                    self.change_y = 0

            if not map[round(self.rect.y / 25)][round(self.rect.x / 25) - 1] in variable and self.change_x < 0:
                if fabs(round(self.rect.x / 25) * 25 - self.rect.x) < 2:
                    self.rect.topleft = (round(self.rect.x / 25) * 25, self.rect.y)
                    self.change_x = 0

            elif not map[round(self.rect.y / 25)][round(self.rect.x / 25) + 1] in variable and self.change_x > 0:
                if fabs(round(self.rect.x / 25) * 25 - self.rect.x) < 2:
                    self.rect.topleft = (round(self.rect.x / 25) * 25, self.rect.y)
                    self.change_x = 0
        except IndexError:
            pass

        if not self.explosion:
            if self.rect.right < 0:
                self.rect.left = SCREEN_WIDTH
            elif self.rect.left > SCREEN_WIDTH:
                self.rect.right = 0
            if self.rect.bottom < 0:
                self.rect.top = SCREEN_HEIGHT
            elif self.rect.top > SCREEN_HEIGHT:
                self.rect.bottom = 0
            self.rect.x += self.change_x
            self.rect.y += self.change_y

            # spritecollide, когда пакман сталкивается со стенкой

            for block in pygame.sprite.spritecollide(self, horizontal_blocks, False):
                self.rect.centery = block.rect.centery
            for block in pygame.sprite.spritecollide(self, vertical_blocks, False):
                self.rect.centerx = block.rect.centerx

            # анимация

            if self.change_x > 0:
                self.move_right_animation.update(10)
                self.image = self.move_right_animation.get_current_image()
            elif self.change_x < 0:
                self.move_left_animation.update(10)
                self.image = self.move_left_animation.get_current_image()

            if self.change_y > 0:
                self.move_down_animation.update(10)
                self.image = self.move_down_animation.get_current_image()
            elif self.change_y < 0:
                self.move_up_animation.update(10)
                self.image = self.move_up_animation.get_current_image()
        else:
            if self.explosion_animation.index == self.explosion_animation.get_length() - 1:
                pygame.time.wait(500)
                self.round_over = True
            self.explosion_animation.update(12)
            self.image = self.explosion_animation.get_current_image()

    def move_right(self):
        self.future_right = True

    def move_left(self):
        self.future_left = True

    def move_up(self):
        self.future_up = True

    def move_down(self):
        self.future_down = True


class Animation(object):
    def __init__(self, img, width, height):
        self.sprite_sheet = img
        # список с изображениями
        self.image_list = []
        self.load_images(width, height)
        self.index = 0
        # время
        self.clock = 1

    def load_images(self, width, height):
        for y in range(0, self.sprite_sheet.get_height(), height):
            for x in range(0, self.sprite_sheet.get_width(), width):
                # загрузка изображений
                img = self.get_image(x, y, width, height)
                self.image_list.append(img)

    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))
        return image

    def get_current_image(self):
        return self.image_list[self.index]

    def get_length(self):
        return len(self.image_list)

    def update(self, fps=30):
        step = 30 // fps
        l = range(1, 30, step)
        if self.clock == 30:
            self.clock = 1
        else:
            self.clock += 1

        if self.clock in l:
            self.index += 1
            if self.index == len(self.image_list):
                self.index = 0
