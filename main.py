import pygame
from game import Game
from characteristic import *


def main():
    pygame.init()
    # ширина, высота окна
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # заголовок окна
    pygame.display.set_caption("PACMAN")
    done = False
    clock = pygame.time.Clock()
    game = Game()
    while not done:
        # --- клики, нажатие клавиш
        done = game.process_events()
        # --- логика игры
        game.run_logic()
        game.display_frame(screen)
        clock.tick(30)
        # tkMessageBox.showinfo("GAME OVER!","Final Score = "+(str)(GAME.score))
    pygame.quit()


if __name__ == '__main__':
    main()
