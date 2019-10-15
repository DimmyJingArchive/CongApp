from screens import util


def main(screen, clock):
    screen.fill([255, 0, 0])
    while True:
        if not util.tick(clock):
            return False
