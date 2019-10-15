import pygame
from screens import util


def main(screen, clock):
    bg = util.get_image('background')
    bg_h = 934
    logo = util.get_image('logo')
    start = util.get_image('start_button')
    start = pygame.transform.scale(start, (350, 150))
    option = util.get_image('options_button')
    option = pygame.transform.scale(option, (400, 150))

    bg_animation_ticks = 200
    bg_ease = util.EaseOutSine(bg_animation_ticks, util.HEIGHT - bg_h, 0)
    logo_ease = util.EaseOutSine(bg_animation_ticks, -50, -160)

    for i in range(bg_animation_ticks):
        # Initialize & scroll start screen
        screen.fill([0, 255, 0])
        screen.blit(bg, (0, next(bg_ease)))
        screen.blit(logo, (0, next(logo_ease)))

        if not util.tick(clock):
            return False

    for i in range(0, 200):
        start.set_alpha(i/20)  # doesn't make the image fully opaque
        option.set_alpha(i/20)
        screen.blit(start, (450, 350))
        screen.blit(option, (420, 500))
        if not util.tick(clock):
            return False

    while True:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        print(click)
        x = 450
        y = 350
        w = 350
        h = 150
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            if click[0] == 1:
                return True
        if not util.tick(clock):
            return False
