import pygame

from screens import util


GRID_COLOR = (0xbf, 0xa3, 0x44)
GRID_SPACE = 110


# 0 for nothing, 1 for knight, 2 for lance, 3 for wizard
char_state = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
# 0 for nothing, 1 for potion, 2 for dragon, 3 for phoenix
# 4 for knight, 5 for lance, 6 for wizard
card_state = [1, 2, 3, 1, 2, 3, 4, 4, 5, 5, 6, 6, 6]


def get_pos(offset, grid_pos):
    return (offset[0] + GRID_SPACE * grid_pos[0] -
            (GRID_SPACE / 5) * grid_pos[1],
            offset[1] + 82 * grid_pos[1] + 214)


def main(screen, clock):
    # Backgrounds
    ground = util.get_image('game_ground')
    card_inventory = util.get_image('card_inventory')
    game_background = util.get_image('game_background')
    # Cards
    card_back = util.get_image('card_back', scale=(100, 108))
    card_border = util.get_image('card_border', scale=(100, 108))
    potion_image = util.get_image('Cards/potion', scale=(70, 70))
    dragon_image = util.get_image('Cards/dragon', scale=(70, 70))
    phoenix_image = util.get_image('Cards/phoenix', scale=(70, 70))
    knight_image = util.get_image('Cards/knight', scale=(70, 70))
    lance_image = util.get_image('Cards/lance', scale=(70, 70))
    wizard_image = util.get_image('Cards/wizard', scale=(70, 70))
    # Character
    knight_idle = [util.get_image(f'Characters/knight/idle_{i+1}', scale=.06)
                   for i in range(4)]
    lance_idle = [util.get_image(f'Characters/lance/idle_{i+1}', scale=.08)
                  for i in range(4)]
    wizard_idle = [util.get_image(f'Characters/wizard/idle_{i+1}', scale=.16)
                  for i in range(4)]
    # Background X Coordinates
    x_g = 0
    x_bg = 0
    # Card Inventory
    screen.blit(card_inventory, (0, 0))
    # Draw grid into surface
    display_grid_hor = False
    display_grid_ver = False
    grid_hor = pygame.Surface((1280, 410))
    grid_ver = pygame.Surface((1280, 410))
    for i in range(11):
        pygame.draw.line(grid_ver, GRID_COLOR,
                         (i * GRID_SPACE + GRID_SPACE + 10, 10),
                         (i * GRID_SPACE + 10, 400), width=10)
    for i in range(4):
        pygame.draw.line(grid_hor, GRID_COLOR, (0, 82 * (i + 1)),
                         (1280, 82 * (i + 1)), width=10)
    grid_hor.set_alpha(100)
    grid_ver.set_alpha(100)
    # Draw cards into their own surfaces,
    cards = [pygame.Surface((90, 90)) for _ in range(6)]
    for i in cards:
        i.blit(card_back, (-8, -8))
    cards[0].blit(potion_image, (10, 8))
    cards[1].blit(dragon_image, (10, 8))
    cards[2].blit(phoenix_image, (10, 8))
    cards[3].blit(knight_image, (10, 8))
    cards[4].blit(lance_image, (10, 8))
    cards[5].blit(wizard_image, (10, 8))
    for i in cards:
        i.blit(card_border, (-8, -8))
    # Character offsets
    knight_idle_offset = (70, -120)
    lance_idle_offset = (65, -80)
    wizard_idle_offset = (100, -100)
    # Game loop
    count = 0
    frame = 0
    # Drag state
    drag_state = (False,)
    card_update = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[1] >= 624:
                    card_num = -1
                    for i in range(len(card_state)):
                        num = len(card_state) - i - 1
                        if pos[0] >= num * 97 + 15:
                            card_num = card_state[num]
                            card_state[num] = 0
                            break
                    if card_num != 0:
                        drag_state = (True, (pos[0] - (num * 97 + 15),
                                             pos[1] - 627), card_num)
                        if card_num == 2:
                            display_grid_hor = True
                        elif card_num > 3:
                            display_grid_hor = True
                            display_grid_ver = True
                    else:
                        drag_state = (False,)
            elif event.type == pygame.MOUSEBUTTONUP:
                if drag_state[0] and drag_state[2] > 3:
                    pos = pygame.mouse.get_pos()
                    x_pos = -1
                    y_pos = -1
                    for i in range(len(char_state)):
                        num = len(char_state) - i - 1
                        if pos[1] >= num * 82 + 214:
                            y_pos = num
                            break
                    for i in range(len(char_state[0])):
                        num = len(char_state[0]) - i - 1
                        if (pos[0] >= (num * GRID_SPACE + 122 - y_pos *
                                       (GRID_SPACE / 5))):
                            x_pos = num
                            break
                    char_state[y_pos][x_pos] = drag_state[2] - 3
                drag_state = (False,)
                display_grid_hor = False
                display_grid_ver = False
                card_update = False
        # Drag State
        if drag_state[0]:
            card_update = False
        # Update Frame
        count += 1
        if count % 13 == 0:
            frame = (frame + 1) % 4
        # Update Cards
        if not card_update:
            card_update = True
            screen.blit(card_inventory, (0, 0))
            for ii, i in enumerate(card_state):
                if i > 0:
                    screen.blit(cards[i - 1], (97 * ii + 15, 624))
        # Scroll the background
        x_g = util.scroll(screen, ground, x_g, 2)
        x_bg = util.scroll(screen, game_background, x_bg, 2, 13129)

        # Grid
        if display_grid_hor:
            screen.blit(grid_hor, (0, 214))
        if display_grid_ver:
            screen.blit(grid_ver, (0, 214))

        # Character
        for ii, i in enumerate(char_state):
            for jj, j in enumerate(i):
                if j == 1:
                    screen.blit(knight_idle[frame],
                                get_pos(knight_idle_offset, (jj, ii)))
                if j == 2:
                    screen.blit(lance_idle[frame],
                                get_pos(lance_idle_offset, (jj, ii)))
                if j == 3:
                    screen.blit(wizard_idle[frame],
                                get_pos(wizard_idle_offset, (jj, ii)))

        # Update Drag
        if drag_state[0]:
            screen.blit(cards[drag_state[2] - 1],
                        (pygame.mouse.get_pos()[0] - drag_state[1][0],
                         pygame.mouse.get_pos()[1] - drag_state[1][1]))

        if not util.tick(clock, False):
            return False
