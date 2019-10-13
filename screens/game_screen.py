from screens import util


def main(screen, clock):
    while True:
        if not util.tick(clock):
            return False
