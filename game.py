import pygame
from player import Player
from enemies import *
from PIL import Image
SCREEN_WIDTH = 475
SCREEN_HEIGHT = 625

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
FORMAT = "RGBA"


class Game(object):
    def __init__(self):
        self.font2 = pygame.font.Font(None, 25)
        self.about = False
        self.game_over = True
        # переменная для очков
        self.score = 0
        # шрифт для показа очков
        self.font = pygame.font.Font(None, 35)
        # меню игры
        self.menu = Menu(("Start", "About", "Exit"), font_color=WHITE, font_size=60)
        # сам пакман
        self.player = Player(9 * 25, 18 * 25, "player.png")
        # блоки где пакман будет ходить
        self.horizontal_blocks = pygame.sprite.Group()
        self.vertical_blocks = pygame.sprite.Group()
        # сами точки для съедения
        self.dots_group = pygame.sprite.Group()
        # добавление блоков:
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item == 1 or item == 20:
                    self.horizontal_blocks.add(Block(j * 25 + 4, i * 25 + 4, BLACK, 16, 16))
                elif item == 16:
                    self.vertical_blocks.add(Block(j * 25 + 4, i * 25 + 4, BLACK, 16, 16))

        # создание привидения
        self.enemies = pygame.sprite.Group()
        # self.enemies.add(Slime(288,96,0,2))
        # self.enemies.add(Slime(288,320,0,-2))
        # self.enemies.add(Slime(544,128,0,2))
        # self.enemies.add(Slime(32,224,0,2))
        # self.enemies.add(Slime(160,64,2,0))
        # self.enemies.add(Slime(448,64,-2,0))
        # self.enemies.add(Slime(640,448,2,0))
        # self.enemies.add(Slime(448,320,2,0))
        # добавление точек
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item == 1 or item == 16 or item == 19:
                    self.dots_group.add(Ellipse(j * 25 + 8, i * 25 + 8, WHITE, 8, 8))

        # Load the sound effects
        self.pacman_sound = pygame.mixer.Sound("pacman_sound.ogg")
        self.game_over_sound = pygame.mixer.Sound("game_over_sound.ogg")

    def process_events(self):
        for event in pygame.event.get():  # если ты что-то нажал
            if event.type == pygame.QUIT:
                return True
            self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_over and not self.about:
                        if self.menu.state == 0:
                            # ---- START ------
                            self.__init__()
                            self.game_over = False
                        elif self.menu.state == 1:
                            # --- ABOUT ------
                            self.about = True
                        elif self.menu.state == 2:
                            # --- EXIT -------
                            return True

                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()

                elif event.key == pygame.K_LEFT:
                    self.player.move_left()

                elif event.key == pygame.K_UP:
                    self.player.move_up()

                elif event.key == pygame.K_DOWN:
                    self.player.move_down()

                elif event.key == pygame.K_ESCAPE:
                    self.game_over = True
                    self.about = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.stop_move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.stop_move_left()
                elif event.key == pygame.K_UP:
                    self.player.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.stop_move_down()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.explosion = True

        return False

    def run_logic(self):
        if not self.game_over:
            self.player.update(self.horizontal_blocks, self.vertical_blocks)
            block_hit_list = pygame.sprite.spritecollide(self.player, self.dots_group, True)
            # когда block_hit_list содержит один спрайт это значит что игрок попал в точку
            if len(block_hit_list) > 0:
                self.pacman_sound.play()
                self.score += 1
            block_hit_list = pygame.sprite.spritecollide(self.player, self.enemies, True)
            if len(block_hit_list) > 0:
                self.player.explosion = True
                self.game_over_sound.play()
            self.game_over = self.player.game_over
            self.enemies.update(self.horizontal_blocks, self.vertical_blocks)

    def display_frame(self, screen):
        screen.fill(BLACK)
        # рисование
        if self.game_over:
            if self.about:
                self.display_message(screen, ["Controlling Pac-Man, eat all the dots in the maze",
                                              "avoiding the ghosts that are chasing the hero."])
            else:
                self.menu.display_frame(screen)
        else:
            self.horizontal_blocks.draw(screen)
            self.vertical_blocks.draw(screen)
            draw_enviroment(screen)
            self.dots_group.draw(screen)
            self.enemies.draw(screen)
            screen.blit(self.player.image, self.player.rect)
            # text=self.font.render("Score: "+(str)(self.score), 1,self.RED)
            # screen.blit(text, (30, 650))
            # Render the text for the score
            text = self.font.render("Score: " + str(self.score), True, GREEN)
            # Put the text on the screen
            screen.blit(text, [120, 20])

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    def display_message(self, screen, message, color=(255, 0, 0)):
        for index, item in enumerate(message):
            label = self.font2.render(item, True, color)

            width = label.get_width()
            height = label.get_height()

            posX = (SCREEN_WIDTH / 2) - (width / 2)
            t_h = len(message) * height
            posY = (SCREEN_HEIGHT / 2) - (t_h / 2) + (index * height)

            screen.blit(label, (posX, posY))


class Menu(object):
    state = 0

    def __init__(self, items, font_color=(0, 0, 0), select_color=(255, 0, 0), ttf_font=None, font_size=25):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font, font_size)
        self.logo = pygame.image.load('logo.png')
        self.image = pygame.image.load('pac.jpg')

    def display_frame(self, screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                label = self.font.render(item, True, self.select_color)
            else:
                label = self.font.render(item, True, self.font_color)

            width = label.get_width()
            height = label.get_height()

            posX = (SCREEN_WIDTH / 2) - (width / 2)
            t_h = len(self.items) * height
            posY = (SCREEN_HEIGHT / 2) - (t_h / 2) + (index * height)

            screen.blit(self.logo, (35, 80))
            screen.blit(self.image, (30, 420))
            screen.blit(label, (posX, posY))

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif event.key == pygame.K_DOWN:
                if self.state < len(self.items) - 1:
                    self.state += 1
