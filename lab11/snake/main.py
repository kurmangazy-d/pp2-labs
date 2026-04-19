import pygame
import random
import sys

#настройки окна
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
CELL_SIZE = 20

COLS = WINDOW_WIDTH // CELL_SIZE
ROWS = WINDOW_HEIGHT // CELL_SIZE

#цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 180, 0)
YELLOW = (255, 255, 0)
RED = (220, 0, 0)
BLUE = (0, 100, 255)
PURPLE = (180, 0, 180)
GRAY = (100, 100, 100)

FPS = 8

#сколько времени еда будет лежать в экране
FOOD_LIFETIME = 5000  



def draw_text(screen, text, size, color, x, y):
    font = pygame.font.SysFont("Arial", size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_grid(screen):
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WINDOW_WIDTH, y))


def draw_snake(screen, snake):
    for i, segment in enumerate(snake):
        rect = pygame.Rect(
            segment[0] * CELL_SIZE,
            segment[1] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )

        
        if i == 0:
            pygame.draw.rect(screen, YELLOW, rect)
        else:
            pygame.draw.rect(screen, GREEN, rect)

        pygame.draw.rect(screen, BLACK, rect, 1)


def draw_food(screen, food):
    x, y = food["pos"]
    weight = food["weight"]

    rect = pygame.Rect(
        x * CELL_SIZE,
        y * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )

    if weight == 1:
        color = RED
    elif weight == 2:
        color = BLUE
    else:
        color = PURPLE

    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)


def generate_food(snake):
    while True:
        x = random.randint(0, COLS - 1)
        y = random.randint(0, ROWS - 1)

        if (x, y) not in snake:
            weight = random.choice([1, 2, 3])

            created_time = pygame.time.get_ticks()

            return {
                "pos": (x, y),
                "weight": weight,
                "created_time": created_time
            }


def show_game_over(screen, score):
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER", 48, RED, 180, 220)
    draw_text(screen, f"Score: {score}", 32, WHITE, 240, 290)
    draw_text(screen, "Press any key to exit", 28, WHITE, 170, 360)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake with Weighted Food")
    clock = pygame.time.Clock()

    
    snake = [(5, 5), (4, 5), (3, 5)]

    dx = 1
    dy = 0

    score = 0

    food = generate_food(snake)

    running = True
    while running:
        #события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -1
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, 1
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -1, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = 1, 0


        current_time = pygame.time.get_ticks()

        if current_time - food["created_time"] > FOOD_LIFETIME:
            food = generate_food(snake)

        
        head_x, head_y = snake[0]
        new_head = (head_x + dx, head_y + dy)

        if new_head[0] < 0 or new_head[0] >= COLS or new_head[1] < 0 or new_head[1] >= ROWS:
            break

        if new_head in snake:
            break

        snake.insert(0, new_head)

    
        if new_head == food["pos"]:
            score += food["weight"]

            food = generate_food(snake)
        else:
            snake.pop()

    
        screen.fill(BLACK)
        draw_grid(screen)
        draw_snake(screen, snake)
        draw_food(screen, food)

        
        draw_text(screen, f"Score: {score}", 28, WHITE, 10, 10)

    
        draw_text(screen, f"Food weight: {food['weight']}", 24, WHITE, 10, 40)

        
        time_left = max(0, (FOOD_LIFETIME - (current_time - food["created_time"])) // 1000)
        draw_text(screen, f"Food timer: {time_left}", 24, WHITE, 10, 70)

        pygame.display.flip()
        clock.tick(FPS)

    show_game_over(screen, score)
    pygame.quit()


if __name__ == "__main__":
    main()