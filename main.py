import pygame

from screens import start_screen
from screens import game_screen
from screens import second_start_screen
from screens import map_screen
from screens import card_screen
from screens import item_screen
from screens import lose_screen

HEIGHT = 720
WIDTH = 1280


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Pig Quest')

    clock = pygame.time.Clock()

    game_screen.init()
    
    state = start_screen.main(screen, clock)
    if not state:
        return
        
    while True:
        state, data = second_start_screen.main(screen, clock)
        if data == 0:
            # Map
            state, temp = map_screen.main(screen, clock)
            state, counting_text = game_screen.main(screen, clock)
            if not state:
                state = lose_screen.main(screen, clock, counting_text)
        elif data == 1:
            # Cards
            state, return_value = card_screen.main(screen, clock)
            if return_value == 0:
                continue
        else:
            # Item select
            state, return_value = item_screen.main(screen, clock)
            if return_value == 0:
                continue

        if not state:
            return
    
    state = game_screen.main(screen, clock)
    if not state:
        return


if __name__ == '__main__':
    main()
