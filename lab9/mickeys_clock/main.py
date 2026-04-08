import pygame
from clock import MickeyClock

#настройка окна
pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Mickey's Clock")
clock = pygame.time.Clock()

center = (200, 200)
mickey_clock = MickeyClock(screen, center)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  #белый фон
    mickey_clock.update()         #обновление
    pygame.display.flip()          

    clock.tick(1)  #обновление каждую секунду

pygame.quit()