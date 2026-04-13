import pygame
from clock import MickeyClock


def main():
    pygame.init()

    WIDTH = 500
    HEIGHT = 500

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey Clock")

    clock = pygame.time.Clock()

    app = MickeyClock(WIDTH, HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        app.update()
        app.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()