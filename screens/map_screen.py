import pygame
from screens import util

def main(screen, clock):
    bg = util.get_image('map_selection_background')

    bg = pygame.transform.scale(bg, (1280, 720))
    select_button_left = util.get_image('select_button_left')
    select_button_left = pygame.transform.scale(select_button_left, (150, 150))
    select_button_right = util.get_image('select_button_right')
    select_button_right = pygame.transform.scale(select_button_right, (150, 150))
    play_button = util.get_image('play_button')
    play_button = pygame.transform.scale(play_button, (350, 150))
    return_button = util.get_image('return_button')
    return_button = pygame.transform.scale(return_button, (175, 60))

    screen.blit(bg, (0,0))
    screen.blit(select_button_left, (50, 280))
    screen.blit(select_button_right, (1100, 280))
    screen.blit(play_button, (460, 550))
    screen.blit(return_button, (1080, 640))

    while True:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 1100+150 > mouse[0] > 1100 and 280+150 > mouse[1] > 280:
            if click[0] == 1:
                screen.blit(play_button, (200, 200))
        if 460+350 > mouse[0] > 460 and 550+150 > mouse[1] > 550:
            if click[0] == 1:
                return True, 0
        if 1080+175 > mouse[0] > 1080 and 640+60 > mouse[1] > 640:
            if click[0] == 1:
                return True, 1
        if not util.tick(clock):
            return False, -1
