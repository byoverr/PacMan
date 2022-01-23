import pygame
from enemies import enviroment

SCREEN_WIDTH = 475
SCREEN_HEIGHT = 625

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    explosion = False
    game_over = False

    def __init__(self, x, y, filename):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        img = pygame.image.load("walk.png").convert()
        # создание анимации
        self.move_right_animation = Animation(img, 25, 25)
        self.move_left_animation = Animation(pygame.transform.flip(img, True, False), 25, 25)
        self.move_up_animation = Animation(pygame.transform.rotate(img, 90), 25, 25)
        self.move_down_animation = Animation(pygame.transform.rotate(img, 270), 25, 25)
        # загрузка взрыва пакмана
        img = pygame.image.load("explosion.png").convert()
        self.explosion_animation = Animation(img, 25, 25)
        self.player_image = pygame.image.load(filename).convert()
        self.player_image.set_colorkey(BLACK)

    def update(self, horizontal_blocks, vertical_blocks):
        variable = [1, 16, 19, 20]

        map = enviroment()
        try:
            if not map[round(self.rect.y / 25) - 1][round(self.rect.x / 25)] in variable and self.change_y < 0:
                if round(self.rect.y / 25) * 25 - self.rect.y > 2:
                    self.rect.topleft = (self.rect.x, round(self.rect.y / 25) * 25)
                    self.change_y = 0

            elif not map[round(self.rect.y / 25) + 1][round(self.rect.x / 25)] in variable and self.change_y > 0:
                if round(self.rect.y / 25) * 25 - self.rect.y < 2:
                    self.rect.topleft = (self.rect.x, round(self.rect.y / 25) * 25)
                    self.change_y = 0

            if not map[round(self.rect.y / 25)][round(self.rect.x / 25) - 1] in variable and self.change_x < 0:
                if round(self.rect.x / 25) * 25 - self.rect.x > 2:
                    self.rect.topleft = (round(self.rect.x / 25) * 25, self.rect.y)
                    self.change_x = 0

            elif not map[round(self.rect.y / 25)][round(self.rect.x / 25) + 1] in variable and self.change_x > 0:
                if round(self.rect.x / 25) * 25 - self.rect.x < 2:
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
                self.change_y = 0
            for block in pygame.sprite.spritecollide(self, vertical_blocks, False):
                self.rect.centerx = block.rect.centerx
                self.change_x = 0

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
                self.game_over = True
            self.explosion_animation.update(12)
            self.image = self.explosion_animation.get_current_image()

    def move_right(self):
        self.change_x = 2

    def move_left(self):
        self.change_x = -2

    def move_up(self):
        self.change_y = -2

    def move_down(self):
        self.change_y = 2

    def stop_move_right(self):
        if self.change_x != 0:
            self.image = self.player_image
        # self.change_x = 0

    def stop_move_left(self):
        if self.change_x != 0:
            self.image = pygame.transform.flip(self.player_image, True, False)
        # self.change_x = 0

    def stop_move_up(self):
        if self.change_y != 0:
            self.image = pygame.transform.rotate(self.player_image, 90)
        # self.change_y = 0

    def stop_move_down(self):
        if self.change_y != 0:
            self.image = pygame.transform.rotate(self.player_image, 270)
        # self.change_y = 0


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
