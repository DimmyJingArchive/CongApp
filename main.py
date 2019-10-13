import pygame

from screens import start_screen
from screens import game_screen


HEIGHT = 720
WIDTH = 1280


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Pig Quest')

    clock = pygame.time.Clock()

    state = start_screen.main(screen, clock)
    if not state:
        return

    state = game_screen.main(screen, clock)
    if not state:
        return


if __name__ == '__main__':
    main()
