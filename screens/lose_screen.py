import pygame
from screens import util

def main(screen, clock):
    lose_screen = util.get_image('lose_screen')
    lose_screen = pygame.transform.scale(lose_screen, (680, 680))
    screen.blit(lose_screen, (300, 20))

    while True:
        if not util.tick(clock):
            return False