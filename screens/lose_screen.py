import pygame
from screens import util

def main(screen, clock, counting_text):
    lose_screen = util.get_image('lose_screen')
    lose_screen = pygame.transform.scale(lose_screen, (680, 680))
    screen.blit(lose_screen, (300, 20))
    screen.blit(counting_text, (600,330))
    font = pygame.font.SysFont(None, 64, italic=True)
    item_text = font.render("2", 1, (43,3,9))
    screen.blit(item_text, (600,375))

    return_button = util.get_image('return_button')
    return_button = pygame.transform.scale(return_button, (175, 60))
    screen.blit(return_button, (710, 560))

    while True:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # x w x, y h y
        if 710+175 > mouse[0] > 710 and 560+60 > mouse[1] > 560:
            if click[0] == 1:
                return True, 0

        if not util.tick(clock):
            return False