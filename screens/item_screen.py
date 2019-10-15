import pygame
from screens import util

def main(screen, clock):
    bg = util.get_image('item_selection_background')
    bg = pygame.transform.scale(bg, (1280, 720))
    return_button = util.get_image('return_button')
    return_button = pygame.transform.scale(return_button, (175, 60))

    screen.blit(bg, (0,0))
    screen.blit(return_button, (1080, 640))

    while True:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # x w x, y h y
        if 1080+175 > mouse[0] > 1080 and 640+60 > mouse[1] > 640:
            if click[0] == 1:
                return True, 0
        if not util.tick(clock):
            return False