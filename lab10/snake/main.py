import pygame
import random
import sys

# ---------------- SETTINGS ----------------
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
CELL_SIZE = 20

# Number of cells
COLS = WINDOW_WIDTH // CELL_SIZE
ROWS = WINDOW_HEIGHT // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
RED = (220, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (40, 40, 40)
YELLOW = (255, 215, 0)

# Initial speed
INITIAL_FPS = 8

# How many foods are needed for next level
FOODS_PER_LEVEL = 4


# ---------------- FUNCTIONS ----------------
def draw_text(screen, text, size, color, x, y):
    """Draw text on the screen."""
    font = pygame.font.SysFont("Arial", size)
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def generate_walls(level):
    """
    Generate walls depending on level.
    Level 1: no inner walls
    Level 2: horizontal wall
    Level 3: vertical walls
    """
    walls = []

    if level == 1:
        return walls

    elif level == 2:
        # Horizontal wall in the middle
        for x in range(10, 20):
            walls.append((x, 15))

    elif level >= 3:
        # Two vertical walls
        for y in range(8, 22):
            walls.append((12, y))
            walls.append((17, y))

    return walls


def generate_food(snake, walls):
    """
    Generate food in a random position.
    Food must not appear on snake or on walls.
    """
    while True:
        x = random.randint(0, COLS - 1)
        y = random.randint(0, ROWS - 1)

        if (x, y) not in snake and (x, y) not in walls:
            return (x, y)


def draw_grid(screen):
    """Optional grid for better visibility."""
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, DARK_GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, DARK_GRAY, (0, y), (WINDOW_WIDTH, y))


def draw_snake(screen, snake):
    """Draw snake body."""
    for i, segment in enumerate(snake):
        rect = pygame.Rect(
            segment[0] * CELL_SIZE,
            segment[1] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )

        # Snake head in yellow, body in green
        if i == 0:
            pygame.draw.rect(screen, YELLOW, rect)
        else:
            pygame.draw.rect(screen, GREEN, rect)

        pygame.draw.rect(screen, BLACK, rect, 1)


def draw_food(screen, food):
    """Draw food."""
    rect = pygame.Rect(
        food[0] * CELL_SIZE,
        food[1] * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )
    pygame.draw.rect(screen, RED, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)


def draw_walls(screen, walls):
    """Draw level walls."""
    for wall in walls:
        rect = pygame.Rect(
            wall[0] * CELL_SIZE,
            wall[1] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(screen, GRAY, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)


def show_game_over(screen, score, level):
    """Display game over message."""
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER", 48, RED, 180, 220)
    draw_text(screen, f"Score: {score}", 32, WHITE, 240, 290)
    draw_text(screen, f"Level: {level}", 32, WHITE, 245, 330)
    draw_text(screen, "Press any key to exit", 28, WHITE, 170, 390)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


# ---------------- MAIN GAME ----------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    # Snake starts with 3 segments
    snake = [(5, 5), (4, 5), (3, 5)]

    # Initial movement direction
    dx = 1
    dy = 0

    score = 0
    level = 1
    fps = INITIAL_FPS

    walls = generate_walls(level)
    food = generate_food(snake, walls)

    running = True
    while running:
        # -------- EVENTS --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Prevent snake from reversing into itself
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -1
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, 1
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -1, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = 1, 0

        # -------- MOVE SNAKE --------
        head_x, head_y = snake[0]
        new_head = (head_x + dx, head_y + dy)

        # -------- COLLISION CHECK --------
        # 1. Border collision / leaving playing area
        if (
            new_head[0] < 0 or new_head[0] >= COLS or
            new_head[1] < 0 or new_head[1] >= ROWS
        ):
            break

        # 2. Collision with itself
        if new_head in snake:
            break

        # 3. Collision with wall
        if new_head in walls:
            break

        # Add new head
        snake.insert(0, new_head)

        # -------- FOOD CHECK --------
        if new_head == food:
            score += 1

            # Level up after every FOODS_PER_LEVEL foods
            new_level = score // FOODS_PER_LEVEL + 1
            if new_level > level:
                level = new_level
                fps += 2  # increase speed
                walls = generate_walls(level)

            # Generate new food in valid position
            food = generate_food(snake, walls)

        else:
            # Remove tail if no food eaten
            snake.pop()

        # -------- DRAW --------
        screen.fill(BLACK)
        draw_grid(screen)
        draw_walls(screen, walls)
        draw_snake(screen, snake)
        draw_food(screen, food)

        # Score and level counter
        draw_text(screen, f"Score: {score}", 28, WHITE, 10, 10)
        draw_text(screen, f"Level: {level}", 28, WHITE, 10, 40)
        draw_text(screen, f"Speed: {fps}", 28, WHITE, 10, 70)

        pygame.display.flip()
        clock.tick(fps)

    show_game_over(screen, score, level)
    pygame.quit()


if __name__ == "__main__":
    main()