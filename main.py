import pygame
import os


HEIGHT = 720
WIDTH = 1280


def get_image(path, ext='png'):
    return pygame.image.load(os.path.join('assets', 'image',
                                          f'{path}.{ext}')).convert()


def scroll(win, image, x_pos):
    win.blit(image, (x_pos, 0))
    win.blit(image, (-1280 + x_pos, 0))
    return (x_pos + 1270) % 1280


def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    bg = pygame.transform.scale(get_image('background'), (WIDTH, HEIGHT - 80))
    pygame.display.set_caption('Pig Quest')
    running = True

    x = 0
    clock = pygame.time.Clock()

    while running:
        x = scroll(win, bg, x)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(60)


if __name__ == '__main__':
    main()
