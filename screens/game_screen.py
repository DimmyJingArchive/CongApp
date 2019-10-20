import pygame

from screens import util


GRID_COLOR = (0xbf, 0xa3, 0x44)
GRID_SPACE_HOR = 110
GRID_SPACE_VER = 82
BACKGROUND_HEIGHT = 214
CHAR_FRAMERATE = 13


# 0 for nothing, 1 for knight, 2 for lance,
# 3 for archer, 4 for gunslinger, 5 for wizard
char_id = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
# -1 for idle, 0-3 for attack, 4 for fainting
char_state = [[-1 for __ in range(10)] for _ in range(5)]
# 0 for nothing, 1 for potion, 2 for dragon, 3 for phoenix
# 4 for knight, 5 for lance
# 6 for archer, 7 for gunslinger, 8 for wizard
card_state = [4, 2, 3, 1, 2, 3, 4, 4, 5, 5, 8, 8, 8]
# (enemy_id, x_pos, health, fainted)
# 0 for porc
enemy_state = [[], [], [], [], []]


def get_x_pos(grid_pos):
    return GRID_SPACE_HOR * grid_pos[0] - (GRID_SPACE_HOR / 5) * grid_pos[1]


def get_y_pos(grid_pos):
    return GRID_SPACE_VER * grid_pos[1] + BACKGROUND_HEIGHT


def get_pos(offset, grid_pos):
    return (offset[0] + get_x_pos(grid_pos),
            offset[1] + get_y_pos(grid_pos))


ground = None
card_inventory = None
game_background = None
cards = None
grid_hor = None
grid_ver = None
idle_animations = []
attack_animations = []
enemy_idle_images = []
enemy_health = [50, 10, 100, 150]
char_damage = [10, 30, 10, 30, 70]
char_offsets = (
    (70, -120),   # Knight
    (65, -80),    # Lance
    (),           # Archer
    (),           # Gunsligner
    (100, -100),  # Wizard
)
enemy_idle_offsets = (
    -140,   # Porc
)
knight_range = 150


def init():
    # Backgrounds
    global ground
    ground = util.get_image('game_ground')
    global card_inventory
    card_inventory = util.get_image('card_inventory')
    global game_background
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
    for i, j in (('knight', .06), ('lance', .08), ('archer', None),
                 ('gunslinger', None), ('wizard', .16)):
        if j is None:
            idle_animations.append(None)
            continue
        idle_animations.append([util.get_image(f'Characters/{i}/idle_{k+1}',
                                               scale=j) for k in range(4)])
    for i, j in (('knight', .06), ('lance', None), ('archer', None),
                 ('gunslinger', None), ('wizard', None)):
        if j is None:
            attack_animations.append(None)
            continue
        attack_animations.append([util.get_image(f'Characters/{i}'
                                                 f'/attack_{k+1}',
                                                 scale=j) for k in range(4)])
    for i, j in (('porc', .07),):
        enemy_idle_images.append(util.get_image(f'Characters/{i}/idle',
                                                scale=j))
    # Draw grid into surface
    global grid_hor
    grid_hor = pygame.Surface((1280, 410))
    global grid_ver
    grid_ver = pygame.Surface((1280, 410))
    for i in range(11):
        pygame.draw.line(grid_ver, GRID_COLOR,
                         (i * GRID_SPACE_HOR + GRID_SPACE_HOR + 10, 10),
                         (i * GRID_SPACE_HOR + 10, 400), width=10)
    for i in range(4):
        pygame.draw.line(grid_hor, GRID_COLOR, (0, GRID_SPACE_VER * (i + 1)),
                         (1280, GRID_SPACE_VER * (i + 1)), width=10)
    grid_hor.set_alpha(100)
    grid_ver.set_alpha(100)
    # Draw cards into their own surfaces,
    global cards
    cards = [pygame.Surface((90, 90)) for _ in range(8)]
    for i in cards:
        i.blit(card_back, (-8, -8))
    cards[0].blit(potion_image, (10, 8))
    cards[1].blit(dragon_image, (10, 8))
    cards[2].blit(phoenix_image, (10, 8))
    cards[3].blit(knight_image, (10, 8))
    cards[4].blit(lance_image, (10, 8))
    # cards[5].blit(archer_image, (10, 8))
    # cards[6].blit(gunslinger_image, (10, 8))
    cards[7].blit(wizard_image, (10, 8))
    for i in cards:
        i.blit(card_border, (-8, -8))


def main(screen, clock):
    # Game loop
    frame = 0
    char_frame = 0
    # Background X Coordinates
    x_g = 0
    x_bg = 0
    # States
    drag_state = (False,)
    card_update = False
    display_grid_hor = False
    display_grid_ver = False
    global enemy_state
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
                    for i in range(len(char_id)):
                        num = len(char_id) - i - 1
                        if pos[1] >= get_y_pos((0, num)):
                            y_pos = num
                            break
                    for i in range(len(char_id[0])):
                        num = len(char_id[0]) - i - 1
                        if (pos[0] >= (num * GRID_SPACE_HOR + 122 - y_pos *
                                       (GRID_SPACE_HOR / 5))):
                            x_pos = num
                            break
                    char_id[y_pos][x_pos] = drag_state[2] - 3
                drag_state = (False,)
                display_grid_hor = False
                display_grid_ver = False
                card_update = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    enemy_state[0].append([0, 1280, enemy_health[0], False])
                if event.key == pygame.K_b:
                    enemy_state[1].append([0, 1280, enemy_health[0], False])
                if event.key == pygame.K_c:
                    enemy_state[2].append([0, 1280, enemy_health[0], False])
                if event.key == pygame.K_d:
                    enemy_state[3].append([0, 1280, enemy_health[0], False])
                if event.key == pygame.K_e:
                    enemy_state[4].append([0, 1280, enemy_health[0], False])

        # Drag State
        if drag_state[0]:
            card_update = False

        # Update Frame
        frame += 1
        if frame % CHAR_FRAMERATE == 0:
            char_frame = frame % 4

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
            screen.blit(grid_hor, (0, BACKGROUND_HEIGHT))
        if display_grid_ver:
            screen.blit(grid_ver, (0, BACKGROUND_HEIGHT))

        # Render character and enemy
        for ii, (char, enem) in enumerate(zip(char_id, enemy_state)):
            for jj, j in enumerate(char):
                if j == 1:
                    center = get_x_pos((jj, ii)) + GRID_SPACE_HOR / 2
                    attack = False
                    for k in enem:
                        if k[1] > center and k[1] < center + knight_range:
                            attack = True
                            if (frame % CHAR_FRAMERATE == 0 and
                               char_state[ii][jj] != -1 and
                               ((char_frame - char_state[ii][jj]
                                 + 4) % 4) == 2):
                                k[2] -= char_damage[0]
                    if char_state[ii][jj] == -1 and attack:
                        char_state[ii][jj] = char_frame
                    if not attack:
                        char_state[ii][jj] = -1
                if j > 0:
                    state = char_state[ii][jj]
                    if state == -1:
                        screen.blit(idle_animations[j - 1][char_frame],
                                    get_pos(char_offsets[j - 1], (jj, ii)))
                    elif state > -1 and state < 4:
                        screen.blit(attack_animations[j - 1][(char_frame -
                                                              state + 4) % 4],
                                    get_pos(char_offsets[j - 1], (jj, ii)))
            for jj, j in enumerate(enem):
                if j[2] <= 0:
                    j[1] = -200
                x_cor = util.scroll_e(screen, enemy_idle_images[j[0]],
                                      enemy_idle_offsets[j[0]] +
                                      get_y_pos((0, ii)), j[1], 2)
                enemy_state[ii][jj][1] = x_cor

        # Update Drag
        if drag_state[0]:
            screen.blit(cards[drag_state[2] - 1],
                        (pygame.mouse.get_pos()[0] - drag_state[1][0],
                         pygame.mouse.get_pos()[1] - drag_state[1][1]))

        # Refresh enemy states
        if frame % 1000 == 0:
            for idx, i in enumerate(enemy_state):
                enemy_state[idx] = [j for j in i if j[1] > -100]

        card_state[0] = 4

        if not util.tick(clock, False):
            return False
