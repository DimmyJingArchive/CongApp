import pygame
import random

from screens import util


GRID_COLOR = (0xbf, 0xa3, 0x44)
GRID_SPACE_HOR = 110
GRID_SPACE_VER = 82
BACKGROUND_HEIGHT = 214
CHAR_FRAMERATE = 13
FAINT_FRAMERATE = 3
SCATTER_FRAMES = 50

pygame.init()
font = pygame.font.SysFont(None, 64, italic=True)

# 0 for nothing, 1 for knight, 2 for lance,
# 3 for archer, 4 for gunslinger, 5 for wizard
char_id = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
# -1 for idle, 0-3 for attack, 4-29 for fainting
char_state = [[-1 for __ in range(10)] for _ in range(5)]
# -1 for occupied, 0 for nothing, 1 for potion, 2 for dragon, 3 for phoenix
# 4 for knight, 5 for lance
# 6 for archer, 7 for gunslinger, 8 for wizard
card_state = [0] * 13
# (enemy_id, x_pos, health, state)
# Enemy_id: 0 for porc, 1 for fly, 2 for wraith
# State: -1 for idle, 0-7 for attack, 8-23 for fainting
enemy_state = [[], [], [], [], []]
# (card_id, x_pos, y_pos)
scattered_cards = []
scattered_cards_anim = []


def get_x_pos(grid_pos):
    return GRID_SPACE_HOR * grid_pos[0] - (GRID_SPACE_HOR / 5) * grid_pos[1]


def get_y_pos(grid_pos):
    return GRID_SPACE_VER * grid_pos[1] + BACKGROUND_HEIGHT


def get_pos(offset, grid_pos):
    return (offset[0] + get_x_pos(grid_pos),
            offset[1] + get_y_pos(grid_pos))


def get_scaty():
    return random.randint(BACKGROUND_HEIGHT, 624-90)

def check_lose(char_id):
    for char_rows in char_id:
        for char in char_rows:
            if char >= 1 and char <= 5:
                return False
    return True

ground = None
card_inventory = None
game_background = None
cards = None
grid_hor = None
grid_ver = None
idle_animations = []
attack_animations = []
faint_animations = []
enemy_idle_images = []
enemy_attack_animations = []
enemy_faint_animations = []
enemy_health = [50, 200, 10, 150]
char_damage = [10, 30, 5, 30, 50]
char_offsets = (
    (70, -120),   # Knight
    (65, -80),    # Lance
    (120, -120),  # Archer
    (),           # Gunsligner
    (100, -100),  # Wizard
)
enemy_idle_offsets = (
    -140,   # Porc
    -240,   # Wraith
    -140,   # Fly
)
knight_range = 150
lance_range = 290
archer_range = 800
porc_range = 300
wizard_range = 450
wraith_range = 450
fly_range = 300

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
    archer_image = util.get_image('Cards/archer', scale=(70, 70))
    wizard_image = util.get_image('Cards/wizard', scale=(70, 70))
    # Character
    for i, j in (('knight', .06), ('lance', .08), ('archer', .06),
                 ('gunslinger', None), ('wizard', .16)):
        if j is None:
            idle_animations.append(None)
            continue
        idle_animations.append([util.get_image(f'Characters/{i}/idle_{k+1}',
                                               scale=j) for k in range(4)])
    for i, j in (('knight', .06), ('lance', .08), ('archer', .06),
                 ('gunslinger', None), ('wizard', .16)):
        if j is None:
            attack_animations.append(None)
            continue
        attack_animations.append([util.get_image(f'Characters/{i}'
                                                 f'/attack_{k+1}',
                                                 scale=j) for k in range(4)])
    for i, j in (('porc', .07), ('wraith', .07), ('fly', .07)):
        if i == 'wraith':
            enemy_idle_images.append([util.get_image(f'Characters/{i}/idle_{k+1}',
                                                     scale=j) for k in range(9)])
            continue
        if i == 'fly':
            enemy_idle_images.append([util.get_image(f'Characters/{i}/idle_{k+1}',
                                                     scale=j) for k in range(7)])
            continue
        enemy_idle_images.append(util.get_image(f'Characters/{i}/idle', scale=j))

    for i, j in (('porc', .07), ('wraith', .07), ('fly', .07)):
        if j is None:
            enemy_attack_animations.append(None)
            continue
        if i == 'fly':
            enemy_attack_animations.append([util.get_image(f'Characters/{i}'
                                                           f'/attack_{k+1}',
                                                           scale=j)
                                        for k in range(4)])
            continue
        enemy_attack_animations.append([util.get_image(f'Characters/{i}'
                                                       f'/attack_{k+1}',
                                                       scale=j)
                                        for k in range(8)])
    
    global faint_animations
    global enemy_faint_animations
    faint_animations = [util.get_image(f'Faint/character/{i+1}', scale=.10)
                        for i in range(26)]
    enemy_faint_animations = [util.get_image(f'Faint/enemy/{i+1}', scale=.10)
                              for i in range(16)]
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
    cards[5].blit(archer_image, (10, 8))
    # cards[6].blit(gunslinger_image, (10, 8))
    cards[7].blit(wizard_image, (10, 8))
    for i in cards:
        i.blit(card_border, (-8, -8))


def main(screen, clock):
    char_id[2][5] = 1
    
    start = pygame.time.get_ticks()
    # time = pygame.time.Clock()
    # Game loop
    frame = 0
    char_frame = 0
    enemy_frame = 0
    # Background X Coordinates
    x_g = 0
    x_bg = 0
    # States
    drag_state = (False,)
    card_update = False
    display_grid_hor = False
    display_grid_ver = False
    global enemy_state
    global scattered_cards
    global scattered_cards_anim
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, "-1"
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
                else:
                    pos = pygame.mouse.get_pos()
                    for i in scattered_cards:
                        if (pos[0] >= i[1] and pos[0] <= i[1] + 90 and
                           pos[1] >= i[2] and pos[1] <= i[2] + 90):
                            empty_card = 0
                            for idx, j in enumerate(card_state):
                                if j == 0:
                                    empty_card = idx
                                    break
                            card_state[empty_card] = -1
                            scattered_cards_anim.append([
                                i[0], empty_card,
                                util.EaseOutSine(SCATTER_FRAMES, i[1],
                                                 97 * empty_card + 15),
                                util.EaseOutSine(SCATTER_FRAMES, i[2], 624)])
                            i[1] = -200
                            break

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
                    enemy_state[0].append([0, 1280, enemy_health[0], -1])
                if event.key == pygame.K_b:
                    enemy_state[1].append([0, 1280, enemy_health[0], -1])
                if event.key == pygame.K_c:
                    enemy_state[2].append([0, 1280, enemy_health[0], -1])
                if event.key == pygame.K_d:
                    enemy_state[3].append([0, 1280, enemy_health[0], -1])
                if event.key == pygame.K_e:
                    enemy_state[4].append([0, 1280, enemy_health[0], -1])
                if event.key == pygame.K_f:
                    scattered_cards.append([4, 1280, get_scaty()])
                if event.key == pygame.K_g:
                    scattered_cards.append([5, 1280, get_scaty()])
                if event.key == pygame.K_h:
                    scattered_cards.append([8, 1280, get_scaty()])
                if event.key == pygame.K_i:
                    scattered_cards.append([1, 1280, get_scaty()])
                if event.key == pygame.K_j:
                    scattered_cards.append([2, 1280, get_scaty()])
                if event.key == pygame.K_k:
                    scattered_cards.append([3, 1280, get_scaty()])
                if event.key == pygame.K_l:
                    scattered_cards.append([6, 1280, get_scaty()])
                if event.key == pygame.K_m:
                    enemy_state[0].append([1, 1280, enemy_health[1], -1])
                if event.key == pygame.K_n:
                    enemy_state[1].append([1, 1280, enemy_health[1], -1])
                if event.key == pygame.K_o:
                    enemy_state[2].append([1, 1280, enemy_health[1], -1])
                if event.key == pygame.K_p:
                    enemy_state[3].append([1, 1280, enemy_health[1], -1])
                if event.key == pygame.K_q:
                    enemy_state[4].append([1, 1280, enemy_health[1], -1])

                if event.key == pygame.K_r:
                    enemy_state[0].append([2, 1280, enemy_health[2], -1])
                if event.key == pygame.K_s:
                    enemy_state[1].append([2, 1280, enemy_health[2], -1])
                if event.key == pygame.K_t:
                    enemy_state[2].append([2, 1280, enemy_health[2], -1])
                if event.key == pygame.K_u:
                    enemy_state[3].append([2, 1280, enemy_health[2], -1])
                if event.key == pygame.K_v:
                    enemy_state[4].append([2, 1280, enemy_health[2], -1])

        # Drag State
        if drag_state[0] or len(scattered_cards_anim) != 0:
            card_update = False

        # Update Cards
        if not card_update:
            card_update = True
            screen.blit(card_inventory, (0, 0))
            for ii, i in enumerate(card_state):
                if i > 0:
                    screen.blit(cards[i - 1], (97 * ii + 15, 624))

        # Update Frame
        frame += 1
        if frame % CHAR_FRAMERATE == 0:
            char_frame = (char_frame + 1) % 4
            enemy_frame = (enemy_frame + 1) % 8

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
            for jj, j in enumerate(enem):
                if j[2] <= 0 and j[3] < 8:
                    j[3] = 8
                    #
                if j[0] == 0 and j[3] < 8:
                    center = j[1]
                    attack = False
                    for kk, k in enumerate(reversed(char)):
                        if (k > 0 and j[1] > get_x_pos((9 - kk, ii)) and
                           (j[1] < get_x_pos((9 - kk, ii)) + porc_range) and
                           char_state[ii][9 - kk] < 4):
                            attack = True
                            if (frame % CHAR_FRAMERATE == 0 and
                               j[3] != -1 and j[3] != 8 and
                               ((enemy_frame - j[3] + 8) % 8) == 7):
                                char_state[ii][9 - kk] = 4
                            break
                    if j[3] == -1 and attack:
                        j[3] = enemy_frame
                    if not attack and j[3] < 8:
                        j[3] = -1
                        #
                if j[0] == 2 and j[3] < 8:
                    center = j[1]
                    attack = False
                    for kk, k in enumerate(reversed(char)):
                        if (k > 0 and j[1] > get_x_pos((9 - kk, ii)) and
                           (j[1] < get_x_pos((9 - kk, ii)) + fly_range) and
                           char_state[ii][9 - kk] < 4):
                            attack = True
                            if (frame % CHAR_FRAMERATE == 0 and
                               j[3] != -1 and j[3] != 8 and
                               ((enemy_frame - j[3] + 7) % 7) == 6):
                                char_state[ii][9 - kk] = 4
                            break
                    if j[3] == -1 and attack:
                        j[3] = enemy_frame
                    if not attack and j[3] < 8:
                        j[3] = -1
                        #
                if j[0] == 1 and j[3] < 8:
                    center = j[1]
                    attack = False
                    for kk, k in enumerate(reversed(char)):
                        if (k > 0 and j[1] > get_x_pos((9 - kk, ii)) and
                           (j[1] < get_x_pos((9 - kk, ii)) + wraith_range) and
                           char_state[ii][9 - kk] < 4):
                            attack = True
                            if (frame % CHAR_FRAMERATE == 0 and
                               j[3] != -1 and j[3] != 8 and
                               ((enemy_frame - j[3] + 8) % 8) == 7):
                                char_state[ii][9 - kk] = 4
                            break
                    if j[3] == -1 and attack:
                        j[3] = enemy_frame
                    if not attack and j[3] < 8:
                        j[3] = -1
                if j[3] == -1:
                    if j[0] == 1:
                        j[1] = util.scroll_e(screen, enemy_idle_images[j[0]]
                                            [(enemy_frame - j[3] + 8) % 8],
                                            enemy_idle_offsets[j[0]] +
                                            get_y_pos((0, ii)), j[1], 2)
                    elif j[0] == 2:
                        j[1] = util.scroll_e(screen, enemy_idle_images[j[0]]
                                            [(enemy_frame - j[3] + 4) % 4],
                                            enemy_idle_offsets[j[0]] +
                                            get_y_pos((0, ii)), j[1], 2)
                    else:
                        j[1] = util.scroll_e(screen, enemy_idle_images[j[0]],
                                            enemy_idle_offsets[j[0]] +
                                            get_y_pos((0, ii)), j[1], 2)
                elif j[3] < 8:
                    if j[0] != 2:
                        j[1] = util.scroll_e(screen, enemy_attack_animations[j[0]]
                                            [(enemy_frame - j[3] + 8) % 8],
                                            enemy_idle_offsets[j[0]] +
                                            get_y_pos((0, ii)), j[1], 2)
                    else:
                        j[1] = util.scroll_e(screen, enemy_attack_animations[j[0]]
                                            [(enemy_frame - j[3] + 4) % 4],
                                            enemy_idle_offsets[j[0]] +
                                            get_y_pos((0, ii)), j[1], 2)
                else:
                    j[1] = util.scroll_e(screen,
                                         enemy_faint_animations[j[3] - 8],
                                         enemy_idle_offsets[j[0]] +
                                         get_y_pos((0, ii)), j[1], 0)
                    if frame % FAINT_FRAMERATE == 0:
                        j[3] += 1
                    if j[3] > 22:
                        j[1] = -1000
                        j[3] = -1
            for jj, j in enumerate(char):
                if j == 1:
                    center = get_x_pos((jj, ii)) + GRID_SPACE_HOR / 2
                    attack = False
                    for k in enem:
                        if k[1] > center and k[1] < center + knight_range:
                            attack = True
                            if (frame % CHAR_FRAMERATE == 0 and
                               char_state[ii][jj] != -1 and
                               char_state[ii][jj] < 4 and
                               ((char_frame - char_state[ii][jj]
                                 + 4) % 4) == 2):
                                k[2] -= char_damage[0]
                            break
                    if char_state[ii][jj] == -1 and attack:
                        char_state[ii][jj] = char_frame
                    if not attack and char_state[ii][jj] < 4:
                        char_state[ii][jj] = -1
                elif j == 2:
                    center = get_x_pos((jj, ii)) + GRID_SPACE_HOR / 2
                    attack = False
                    for k in enem:
                        if k[1] > center and k[1] < center + lance_range:
                            attack = True
                            if (frame % CHAR_FRAMERATE == 0 and
                               char_state[ii][jj] != -1 and
                               char_state[ii][jj] < 4 and
                               ((char_frame - char_state[ii][jj]
                                 + 4) % 4) == 3):
                                k[2] -= char_damage[1]
                            break
                    if char_state[ii][jj] == -1 and attack:
                        char_state[ii][jj] = char_frame
                    if not attack and char_state[ii][jj] < 4:
                        char_state[ii][jj] = -1
                elif j == 3:
                    center = get_x_pos((jj, ii)) + GRID_SPACE_HOR / 2
                    attack = False
                    for k in enem:
                        if k[1] > center and k[1] < center + archer_range:
                            attack = True
                            if (frame % CHAR_FRAMERATE == 0 and
                               char_state[ii][jj] != -1 and
                               char_state[ii][jj] < 4 and
                               ((char_frame - char_state[ii][jj]
                                 + 4) % 4) == 3):
                                k[2] -= char_damage[2]
                            break
                    if char_state[ii][jj] == -1 and attack:
                        char_state[ii][jj] = char_frame
                    if not attack and char_state[ii][jj] < 4:
                        char_state[ii][jj] = -1
                elif j == 5:
                    center = get_x_pos((jj, ii)) + GRID_SPACE_HOR / 2
                    attack = False
                    for k in enem:
                        if k[1] > center and k[1] < center + wizard_range:
                            attack = True
                            if (frame % CHAR_FRAMERATE == 0 and
                               char_state[ii][jj] != -1 and
                               char_state[ii][jj] < 4 and
                               ((char_frame - char_state[ii][jj]
                                 + 4) % 4) == 3):
                                k[2] -= char_damage[4]
                            break
                    if char_state[ii][jj] == -1 and attack:
                        char_state[ii][jj] = char_frame
                    if not attack and char_state[ii][jj] < 4:
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
                    else:
                        screen.blit(faint_animations[state - 4],
                                    get_pos(char_offsets[j - 1], (jj, ii)))
                        if frame % FAINT_FRAMERATE == 0:
                            char_state[ii][jj] += 1
                        if char_state[ii][jj] > 29:
                            char_id[ii][jj] = 0
                            char_state[ii][jj] = -1
        end = pygame.time.get_ticks()
        counting_time = end - start
        
        counting_text = font.render(str("{:.1f}m".format(counting_time / 1000)), 1, (43,3,9))
        screen.blit(counting_text, (10,10))

        # Check Lose
        if check_lose(char_id):
            for i in enemy_state:
                i.clear()

            scattered_cards = []
            scattered_cards_anim = []
            return False, counting_text
        # Draw Card
        for i in scattered_cards:
            i[1] = util.scroll_e(screen, cards[i[0]-1], i[2], i[1], 2)

        # Update Drag
        if drag_state[0]:
            screen.blit(cards[drag_state[2] - 1],
                        (pygame.mouse.get_pos()[0] - drag_state[1][0],
                         pygame.mouse.get_pos()[1] - drag_state[1][1]))

        # Refresh enemy states
        if frame % 1000 == 0:
            for idx, i in enumerate(enemy_state):
                enemy_state[idx] = [j for j in i if j[1] > -100]
            scattered_cards = [i for i in scattered_cards if i[1] > -100]
            scattered_cards_anim = [i for i in scattered_cards_anim
                                    if i[0] is not None]

        # Animate scattered cards
        for i in scattered_cards_anim:
            if i[0] is not None:
                try:
                    screen.blit(cards[i[0]-1], (next(i[2]), next(i[3])))
                except StopIteration:
                    card_state[i[1]] = i[0]
                    screen.blit(cards[i[0]-1], (97 * i[1] + 15, 624))
                    i[0] = None
                    card_update = False

        if not util.tick(clock, False):
            return False, counting_text