import time
import pygame
import sqlite3
from player import Player
from enemies import *
from characteristic import *
from threading import Thread
pygame.init()
pygame.joystick.init()
joystick = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
# ширина, высота окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Game(object):
    def __init__(self, chek_start=False):
        self.chek_start = chek_start
        self.score_live = 0
        self.run = True
        self.not_was_win = True
        self.orange_scare = False
        self.red_scare = False
        self.pink_scare = False
        self.blue_scare = False
        self.enemies_list = []
        self.eat_ghost = False
        self.cheat_joy = ''
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
        self.font = pygame.font.Font('data/fgr2.ttf', 25)
        self.font2 = pygame.font.Font('data/fgr2.ttf', 25)
        # меню игры
        self.menu = Menu(("Start", "Exit"), font_color=WHITE, font_size=45, ttf_font='data/fgr2.ttf')
        # сам пакман
        self.player = Player(9 * 25, 18 * 25, "data/player.png")
        # блоки где пакман будет ходить
        self.horizontal_blocks = pygame.sprite.Group()
        self.vertical_blocks = pygame.sprite.Group()
        # сами точки для съедения
        self.dots_group = pygame.sprite.Group()
        self.dots_for_eat = pygame.sprite.Group()
        # добавление блоков:
        Thread(target=self.run_func).start()

        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item == 1 or item == 20:
                    self.horizontal_blocks.add(Block(j * 25 + 4, i * 25 + 4, BLACK, 16, 16))
                elif item == 16:
                    self.vertical_blocks.add(Block(j * 25 + 4, i * 25 + 4, BLACK, 16, 16))

        # создание привидения
        # создание привидения
        self.enemies = pygame.sprite.Group()
        self.B = Blinky(9 * 25, 10 * 25, 0, 0)
        self.P = Pinky(9 * 25, 12 * 25, 0, 0)
        self.I = Inky(10 * 25, 12 * 25, 0, 0)
        self.C = Clyde(8 * 25, 12 * 25, 0, 0)
        self.enemies.add(self.B, self.P, self.I, self.C)

        # добавление точек
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item == 1 or item == 16 or item == 19:
                    self.all_dots += 1
                    self.dots_group.add(Ellipse(j * 25 + 9.5, i * 25 + 9.5, WHITE, 6, 6))
                elif item == 21 or item == 23:
                    # Berry
                    self.all_dots += 1
                    self.dots_for_eat.add(Ellipse(j * 25 + 6.5, i * 25 + 6.5, WHITE, 12, 12))

        # Load the sound effects
        self.pacman_sound = pygame.mixer.Sound("data/pacman_sound.ogg")
        self.game_over_sound = pygame.mixer.Sound("data/game_over_sound.ogg")
        self.win_sound = pygame.mixer.Sound("data/win.mp3")
        self.eat_ghost_sound = pygame.mixer.Sound("data/an-nam.mp3")

    def win(self):
        self.not_was_win = False
        self.win_sound.play()
        time.sleep(6)

    def process_events(self):

        for event in pygame.event.get():  # если ты что-то нажал
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    if round(event.value) == 1:
                        self.player.move_right()
                    elif round(event.value) == -1:
                        self.player.move_left()
                else:
                    if round(event.value) == 1:
                        self.player.move_down()
                    elif round(event.value) == -1:
                        self.player.move_up()
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 7:
                    self.cheat_joy = ''.join(sorted(list(set(list(self.cheat_joy))), key=lambda x: int(x)))
                    if self.cheat_joy == '123':
                        self.round_win = True
                    elif self.cheat_joy == '6':
                        self.player.speed -= 2
                    elif self.cheat_joy == '4':
                        self.player.speed += 2
                    elif self.cheat_joy == '023':
                        self.lives += 1
                    elif self.cheat_joy == '013':
                        change_state = Thread(target=self.eat, args=[100])
                        change_state.start()
                    elif self.cheat_joy == '35':
                        self.score_live += 1000
                        self.score += 1000
                    self.cheat_joy = ''
                else:
                    self.cheat_joy += str(event.button)

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
                        self.__init__(chek_start=True)
                        pygame.mixer.Sound("data/intro.mp3").play()
                        self.score = self.score_round_win
                        self.level = self.level_round_win
                        self.lives = self.lives_round_win
                        self.game_over = False
                        self.round_win = False
                        con = sqlite3.connect('data/records.db')
                        con.cursor().execute(f'''INSERT INTO record(score, level)
                                        VALUES ('{self.score}', '{self.level}')''')
                        con.commit()
                        con.close()
                    elif self.game_over and not self.about:
                        if self.menu.state == 0:
                            # ---- START ------
                            self.__init__(chek_start=True)
                            self.game_over = False
                            self.win_sound.stop()
                            pygame.mixer.Sound("data/intro.mp3").play()

                        elif self.menu.state == 1:
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

    def run_func(self):
        self.run = True
        time.sleep(15)
        self.run = False
        time.sleep(20)

        self.run = True
        time.sleep(7)
        self.run = False
        time.sleep(20)

        self.run = True
        time.sleep(5)
        self.run = False
        time.sleep(20)

        self.run = True
        time.sleep(5)
        self.run = False

    def run_logic(self):
        if self.chek_start:
            self.chek_start = False
            self.display_frame(screen)
            time.sleep(pygame.mixer.Sound("data/intro.mp3").get_length())
        if self.score_live >= 10000:
            self.lives += 1
            self.score_live -= 10000
        if not self.game_over and not self.round_win:
            self.player.update(self.horizontal_blocks, self.vertical_blocks)
            block_hit_list = pygame.sprite.spritecollide(self.player, self.dots_group, True)
            # когда block_hit_list содержит один спрайт это значит что игрок попал в точку
            if len(block_hit_list) > 0:
                self.pacman_sound.play()
                self.score += 10
                self.score_live += 10
                self.all_dots -= 1
                if len(self.dots_group) == 0 and len(self.dots_for_eat) == 0:
                    self.round_win = True

                    self.pacman_sound.stop()
            block_hit_list = pygame.sprite.spritecollide(self.player, self.dots_for_eat, True)
            if len(block_hit_list) > 0:
                pygame.mixer.Sound('data/Extra.mp3').play()
                self.score_live += 50
                self.score += 50
                for i in [self.B, self.I, self.P]:
                    i.change_x = -i.change_x
                    i.change_y = -i.change_y
                change_state = Thread(target=self.eat, args=[5])
                change_state.start()

            my_enemies = []
            for i in self.enemies:
                my_enemies.append(str(type(i)).split('.')[-1][:-2])
            block_hit_list = pygame.sprite.spritecollide(self.player, self.enemies, True)

            if len(block_hit_list) > 0:
                if not self.eat_ghost:

                    self.player.explosion = True
                    self.game_over_sound.play()
                else:
                    self.eat_ghost_sound.stop()
                    self.eat_ghost_sound.play(maxtime=2000)
                    ghosts_now = []
                    for i in self.enemies:
                        ghosts_now.append(str(type(i)).split('.')[-1][:-2])

                    for i in my_enemies:
                        if i not in ghosts_now:
                            if i == 'Blinky' and self.red_scare:
                                answer2 = Thread(target=self.death_ghost, args=[i])
                                answer2.start()
                            elif i == 'Pinky' and self.pink_scare:
                                answer1 = Thread(target=self.death_ghost, args=[i])
                                answer1.start()
                            elif i == 'Inky' and self.blue_scare:
                                answer3 = Thread(target=self.death_ghost, args=[i])
                                answer3.start()
                            elif i == 'Clyde' and self.orange_scare:
                                answer4 = Thread(target=self.death_ghost, args=[i])
                                answer4.start()
                            else:
                                self.player.explosion = True
                                self.game_over_sound.play()

            self.round_over = self.player.round_over
            self.enemies.update(self.horizontal_blocks, self.vertical_blocks, self.player.rect.x, self.player.rect.y,
                                change_x=self.player.change_x, change_y=self.player.change_y, red_x=self.B.rect.x,
                                red_y=self.B.rect.y, scare_red=self.red_scare, scare_pink=self.pink_scare,
                                scare_blue=self.blue_scare, scare_orange=self.orange_scare, run=self.run)

    def death_ghost(self, ghost):
        time.sleep(2)
        if ghost == 'Blinky':
            self.B = Blinky(9 * 25, 12 * 25, 0, 0)
            self.enemies.add(self.B)
            self.red_scare = False
        elif ghost == 'Pinky':
            self.P = Pinky(9 * 25, 12 * 25, 0, 0)
            self.enemies.add(self.P)
            self.pink_scare = False
        elif ghost == 'Inky':
            self.I = Inky(10 * 25, 12 * 25, -1, 0)
            self.enemies.add(self.I)
            self.blue_scare = False
        elif ghost == 'Clyde':
            self.C = Clyde(8 * 25, 12 * 25, 1, 0)
            self.enemies.add(self.C)
            self.orange_scare = False

    def eat(self, timer):
        pygame.mixer.Sound("data/extra.mp3").play()
        count = 0
        self.eat_ghost = True
        self.red_scare = True
        self.orange_scare = True
        self.pink_scare = True
        answer = pygame.mixer.Sound("data/scare_ghost_sound.mp3")
        answer.set_volume(0.1)
        answer.play()
        self.blue_scare = True
        time.sleep(timer)
        for i in [self.red_scare, self.blue_scare, self.pink_scare, self.orange_scare]:
            if i:
                count += 1
        for i in [self.B, self.I, self.P]:
            i.change_x = -i.change_x
            i.change_y = -i.change_y
        self.score += (count ** 2) * 100
        self.score_live += (count ** 2) * 100
        answer.stop()
        self.eat_ghost = False
        self.red_scare = False
        self.pink_scare = False
        self.orange_scare = False
        self.blue_scare = False
        pygame.mixer.Sound("data/non_extra.mp3").play()

    def display_frame(self, screen):
        screen.fill(BLACK)
        # рисование
        if self.round_win:
            con = sqlite3.connect('data/records.db')
            con.cursor().execute(f'''INSERT INTO record(score, level)
                            VALUES ('{self.score}', '{self.level}')''')
            con.commit()
            con.close()
            self.display_message(screen, ["You won the level!",
                                          "Press Enter to continue."])
            if self.not_was_win:
                self.win_sound.stop()
                answer = Thread(target=self.win)
                answer.start()
        elif self.round_over:
            self.lives -= 1

            for i in self.enemies:
                i.kill()
            self.player.explosion = False
            self.eat_ghost = False
            self.red_scare = False
            self.blue_scare = False
            self.orange_scare = False
            self.pink_scare = False
            self.player.image = pygame.image.load('data/player.png').convert()
            self.player.image.set_colorkey(BLACK)
            self.player.rect.topleft = (9 * 25, 18 * 25)
            screen.blit(self.player.image, self.player.rect)
            self.player.round_over = False
            if self.lives == 0:
                self.game_over = True
            else:

                self.B = Blinky(9 * 25, 10 * 25, -4.75, 0)
                self.P = Pinky(9 * 25, 12 * 25, 0, 0)
                self.I = Inky(10 * 25, 12 * 25, -1, 0)
                self.C = Clyde(8 * 25, 12 * 25, 1, 0)
                self.enemies.add(self.B, self.P, self.I, self.C)


        elif self.game_over:
            con = sqlite3.connect('data/records.db')
            con.cursor().execute(f'''INSERT INTO record(score, level)
                            VALUES ('{self.score}', '{self.level}')''')
            con.commit()
            con.close()
            self.menu.display_frame(screen)

        else:
            for i in range(self.lives - 1):
                screen.blit(pygame.image.load('data/player.png'), (30 + (30 * i), 20))

            self.horizontal_blocks.draw(screen)
            self.vertical_blocks.draw(screen)
            draw_enviroment(screen)
            self.dots_group.draw(screen)
            self.dots_for_eat.draw(screen)
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

    def __init__(self, items, font_color=(0, 0, 0), select_color=(255, 0, 0), ttf_font='data/fgr.ttf', font_size=25):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font, font_size)
        self.font2 = pygame.font.Font('data/fgr.ttf', 20)

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
            posY = (SCREEN_HEIGHT * 0.6) - (t_h / 2) + (index * height)

            screen.blit(pygame.image.load('data/W0NFOrs44_Y.jpg'),
                        (SCREEN_WIDTH / 2 - pygame.image.load('data/W0NFOrs44_Y.jpg').get_width() / 2, 70))
            screen.blit(pygame.image.load('data/pac.jpg'),
                        ((SCREEN_WIDTH / 2) - (pygame.image.load('data/pac.jpg').get_width() / 2),
                         (SCREEN_HEIGHT * 0.9) - (pygame.image.load('data/W0NFOrs44_Y.jpg').get_height() / 2)))

            con = sqlite3.connect('data/records.db')
            cur = con.cursor()

            # show record on menu
            max_score = max([j for elem in cur.execute(f'''SELECT score FROM record''').fetchall() for j in elem])
            max_level = max([j for elem in cur.execute(f'''SELECT level FROM record''').fetchall() for j in elem])
            con.close()

            record_score = self.font2.render(f'High score: {max_score}', True, (255, 255, 255))
            record_level = self.font2.render(f'High level: {max_level}', True, (255, 255, 255))
            screen.blit(record_score, (SCREEN_WIDTH / 4 - record_score.get_width() / 2, 20))
            screen.blit(record_level, (SCREEN_WIDTH * 0.75 - record_level.get_width() / 2, 20))

            screen.blit(label, (posX, posY))

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif event.key == pygame.K_DOWN:
                if self.state < len(self.items) - 1:
                    self.state += 1
