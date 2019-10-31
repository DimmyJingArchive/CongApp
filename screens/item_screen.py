import pygame
from screens import util

def main(screen, clock):
    bg = util.get_image('item_selection_background')
    bg = pygame.transform.scale(bg, (1280, 720))
    return_button = util.get_image('return_button')
    return_button = pygame.transform.scale(return_button, (175, 60))

    screen.blit(bg, (0,0))
    screen.blit(return_button, (1080, 640))

    card_back = util.get_image('card_back', scale=(450, 458))
    card_border = util.get_image('card_border', scale=(450, 458))
    potion_image = util.get_image('Cards/potion', scale=(300, 300))
    dragon_image = util.get_image('Cards/dragon', scale=(280, 280))
    phoenix_image = util.get_image('Cards/phoenix', scale=(340, 340))

    # blitting the selction items
    screen.blit(card_back, (-10, 20))
    screen.blit(card_back, (410, 20))
    screen.blit(card_back, (830, 20))

    screen.blit(potion_image, (70, 90))
    screen.blit(dragon_image, (511, 86))
    screen.blit(phoenix_image, (875, 35))

    screen.blit(card_border, (-10, 20))
    screen.blit(card_border, (410, 20))
    screen.blit(card_border, (830, 20))

    # blitting the items selected
    card_back = pygame.transform.scale(card_back, (180, 188))
    card_border = pygame.transform.scale(card_border, (180, 188))
    potion_image = pygame.transform.scale(potion_image, (135, 135))
    dragon_image = pygame.transform.scale(dragon_image, (112, 115))

    screen.blit(card_back, (45, 510))
    screen.blit(card_back, (245, 510))

    screen.blit(potion_image, (75, 540))
    screen.blit(dragon_image, (287, 536))

    screen.blit(card_border, (45, 510))
    screen.blit(card_border, (245, 510))


    while True:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # x w x, y h y
        if 1080+175 > mouse[0] > 1080 and 640+60 > mouse[1] > 640:
            if click[0] == 1:
                return True, 0
        if not util.tick(clock):
            return False