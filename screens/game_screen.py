import pygame

from screens import util


GRID_COLOR = (0xbf, 0xa3, 0x44)
GRID_SPACE = 110


def main(screen, clock):
    ground = util.get_image('game_background')
    card_inventory = util.get_image('card_inventory')
    game_background = util.get_image('game_backgrounds/background1')
    card_back = util.get_image('card_back')
    card_border = util.get_image('card_border')
    x_g = 0
    x_bg = 0

    screen.blit(card_inventory, (0, 0))

    surface = pygame.Surface((1280, 410))
    for i in range(11):
        pygame.draw.line(surface, GRID_COLOR,
                         (i * GRID_SPACE + GRID_SPACE + 10, 10),
                         (i * GRID_SPACE + 10, 400), width=10)
    for i in range(4):
        pygame.draw.line(surface, GRID_COLOR,
                         (0, 82 * (i + 1)), (1280, 82 * (i + 1)), width=10)
    surface.set_alpha(100)

    # potion_card = pygame.Surface(2988, 2900)

    while True:
        x_g = util.scroll(screen, ground, x_g, 2)
        x_bg = util.scroll(screen, game_background, x_bg, 2, 13129)

        screen.blit(surface, (0, 214))

        if not util.tick(clock):
            return False
