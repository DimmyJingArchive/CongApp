from screens import util


def main(screen, clock):
    bg = util.get_image('background')
    bg_h = 934
    logo = util.get_image('logo')

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

    while True:
        if not util.tick(clock):
            return False
