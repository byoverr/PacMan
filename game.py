import pygame
import sqlite3
from player import Player
from enemies import *
from characteristic import *


class Game(object):
    def __init__(self):
        self.about = False
        self.game_over = True
        self.round_over = False
        self.round_win = False
        # переменная для очков
        self.level = 1
        self.lives = 3
        self.score = 0
        self.all_dots = 0
        # шрифт для показа очков
        self.font = pygame.font.Font(None, 35)
        self.font2 = pygame.font.Font(None, 25)
        # меню игры
        self.menu = Menu(("Start", "About", "Exit"), font_color=WHITE, font_size=60)
        # сам пакман
        self.player = Player(9 * 25, 18 * 25, "data/player.png")
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
        self.enemies.add(Blinky(10 * 25, 10 * 25, 2, 0))
        self.enemies.add(Pinky(8 * 25, 10 * 25, -2, 0))

        # добавление точек
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item == 1 or item == 16 or item == 19:
                    self.all_dots += 10
                    self.dots_group.add(Ellipse(j * 25 + 9.5, i * 25 + 9.5, WHITE, 6, 6))
                elif item == 21:
                    self.all_dots += 200
                    self.dots_group.add(Berry(j * 25, i * 25))

        # Load the sound effects
        self.pacman_sound = pygame.mixer.Sound("data/pacman_sound.ogg")
        self.game_over_sound = pygame.mixer.Sound("data/game_over_sound.ogg")

    def process_events(self):
        for event in pygame.event.get():  # если ты что-то нажал
            if event.type == pygame.QUIT:
                return True
            self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.round_win:
                        self.level += 1
                        self.lives_round_win = self.lives
                        self.score_round_win = self.score
                        self.level_round_win = self.level
                        self.__init__()
                        self.score = self.score_round_win
                        self.level = self.level_round_win
                        self.lives = self.lives_round_win
                        self.game_over = False
                        self.round_win = False
                    elif self.game_over and not self.about:
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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.explosion = True

        return False

    def run_logic(self):
        if not self.game_over and not self.round_win:
            self.player.update(self.horizontal_blocks, self.vertical_blocks)
            block_hit_list = pygame.sprite.spritecollide(self.player, self.dots_group, True)
            # когда block_hit_list содержит один спрайт это значит что игрок попал в точку
            if len(block_hit_list) > 0:
                self.pacman_sound.play()
                if str(block_hit_list) == '[<Berry Sprite(in 0 groups)>]':
                    self.score += 200
                else:
                    self.score += 10

                if self.score == self.all_dots:
                    self.round_win = True
            block_hit_list = pygame.sprite.spritecollide(self.player, self.enemies, True)
            if len(block_hit_list) > 0:
                self.player.explosion = True
                self.game_over_sound.play()
            self.round_over = self.player.round_over
            self.enemies.update(self.horizontal_blocks, self.vertical_blocks, self.player.rect.x, self.player.rect.y)

    def display_frame(self, screen):
        screen.fill(BLACK)
        # рисование
        if self.round_win:
            self.display_message(screen, ["You won the level!",
                                          "Press Enter to continue."])
        elif self.round_over:
            self.lives -= 1
            if self.lives == 0:
                self.game_over = True
            self.player.explosion = False
            self.player.image = pygame.image.load('data/player.png').convert()
            self.player.image.set_colorkey(BLACK)
            self.player.rect.topleft = (9 * 25, 18 * 25)
            screen.blit(self.player.image, self.player.rect)
            self.player.round_over = False
        elif self.game_over:
            con = sqlite3.connect('data/records.db')
            con.cursor().execute(f'''INSERT INTO record(score, level)
                            VALUES ('{self.score}', '{self.level}')''')
            con.commit()
            con.close()
            if self.about:
                self.display_message(screen, ["Controlling Pac-Man, eat all the dots in the maze",
                                              "avoiding the ghosts that are chasing the hero."])
            else:
                self.menu.display_frame(screen)
        else:
            for i in range(self.lives - 1):
                screen.blit(pygame.image.load('data/player.png'), (30 + (30 * i), 20))

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
            text2 = self.font.render("Level: " + str(self.level), True, GREEN)
            # Put the text on the screen
            screen.blit(text, [120, 20])
            screen.blit(text2, [300, 20])

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
        self.font2 = pygame.font.Font(None, 40)

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

            screen.blit(pygame.image.load('data/logo.png'), (35, 80))
            screen.blit(pygame.image.load('data/pac.jpg'), (30, 420))

            con = sqlite3.connect('data/records.db')
            cur = con.cursor()

            # show record on menu
            max_score = max([j for elem in cur.execute(f'''SELECT score FROM record''').fetchall() for j in elem])
            max_level = max([j for elem in cur.execute(f'''SELECT level FROM record''').fetchall() for j in elem])
            con.close()

            record_score = self.font2.render(f'Highest score: {max_score}', True, (255, 255, 255))
            record_level = self.font2.render(f'Highest level: {max_level}', True, self.select_color)
            screen.blit(record_score, (130, 500))
            screen.blit(record_level, (130, 550))

            screen.blit(label, (posX, posY))

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif event.key == pygame.K_DOWN:
                if self.state < len(self.items) - 1:
                    self.state += 1
