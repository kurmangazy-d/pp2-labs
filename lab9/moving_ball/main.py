import pygame
from ball import Ball


def main():
    pygame.init()

    WIDTH = 800
    HEIGHT = 600

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Red Ball")

    clock = pygame.time.Clock()

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    ball = Ball(
        x=WIDTH // 2,
        y=HEIGHT // 2,
        radius=25,
        color=RED,
        screen_width=WIDTH,
        screen_height=HEIGHT
    )

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball.move_up()
                elif event.key == pygame.K_DOWN:
                    ball.move_down()
                elif event.key == pygame.K_LEFT:
                    ball.move_left()
                elif event.key == pygame.K_RIGHT:
                    ball.move_right()

        ball.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()