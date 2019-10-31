import pygame
from screens import util

def main(screen, clock):
    bg = util.get_image('card_selection_background')
    bg = pygame.transform.scale(bg, (1280, 720))
    return_button = util.get_image('return_button')
    return_button = pygame.transform.scale(return_button, (175, 60))

    screen.blit(bg, (0,0))
    screen.blit(return_button, (1080, 640))

    card_back = util.get_image('card_back', scale=(200, 208))
    card_border = util.get_image('card_border', scale=(200, 208))
    knight_image = util.get_image('Cards/knight', scale=(100, 100))
    lance_image = util.get_image('Cards/lance', scale=(100, 100))
    archer_image = util.get_image('Cards/archer', scale=(100, 100))
    wizard_image = util.get_image('Cards/wizard', scale=(100, 100))
    
    # bltting card selection list
    screen.blit(card_back, (145, 150))
    screen.blit(card_back, (395, 150))
    screen.blit(card_back, (645, 150))
    screen.blit(card_back, (895, 150))

    screen.blit(knight_image, (190, 185))
    screen.blit(archer_image, (455, 180))
    screen.blit(lance_image, (710, 180))
    screen.blit(wizard_image, (960, 180))

    screen.blit(card_border, (145, 150))
    screen.blit(card_border, (395, 150))
    screen.blit(card_border, (645, 150))
    screen.blit(card_border, (895, 150))

    # blitting card selection
    card_back = pygame.transform.scale(card_back, (90, 98))
    card_border = pygame.transform.scale(card_border, (90, 98))
    knight_image = pygame.transform.scale(knight_image, (45, 49))
    archer_image = pygame.transform.scale(archer_image, (45, 49))
    lance_image = pygame.transform.scale(lance_image, (45, 49))
    wizard_image = pygame.transform.scale(wizard_image, (45, 49))

    screen.blit(card_back, (120, 560))
    screen.blit(card_back, (220, 560))
    screen.blit(card_back, (320, 560))
    screen.blit(card_back, (420, 560))

    screen.blit(knight_image, (149, 590))
    screen.blit(archer_image, (251, 585))
    screen.blit(lance_image, (353, 585))
    screen.blit(wizard_image, (451, 585))

    screen.blit(card_border, (120, 560))
    screen.blit(card_border, (220, 560))
    screen.blit(card_border, (320, 560))
    screen.blit(card_border, (420, 560))

    while True:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # x w x, y h y
        if 1080+175 > mouse[0] > 1080 and 640+60 > mouse[1] > 640:
            if click[0] == 1:
                return True, 0
        if not util.tick(clock):
            return False