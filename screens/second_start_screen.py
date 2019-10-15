import pygame
from screens import util

def main(screen, clock):
    bg = util.get_image('background')

    map_button = util.get_image('maps_button')
    map_button = pygame.transform.scale(map_button, (350, 150))
    cards_button = util.get_image('cards_button')
    cards_button = pygame.transform.scale(cards_button, (350, 150))
    items_button = util.get_image('items_button')
    items_button = pygame.transform.scale(items_button, (350, 150))

    screen.blit(bg, (0,0))
    screen.blit(map_button, (20, 100))
    screen.blit(cards_button, (450, 100))
    screen.blit(items_button, (900, 100))

    while True:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # x w x, y h y
        if 20+350 > mouse[0] > 20 and 100+150 > mouse[1] > 100:
            if click[0] == 1:
                return True, 0
        elif 450+350 > mouse[0] > 450 and 100+150 > mouse[1] > 100:
            if click[0] == 1:
                return True, 1
        elif 900+350 > mouse[0] > 900 and 100+150 > mouse[1] > 100:
            if click[0] == 1:
                return True, 2

        if not util.tick(clock):
            return False, -1
