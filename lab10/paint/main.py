import pygame

# ---------------------------------
# Paint Program with:
# - Brush
# - Rectangle
# - Circle
# - Eraser
# - Color selection
# ---------------------------------


def draw_palette(screen, colors, selected_color, palette_rects, font):
    """Draw color selection boxes."""
    for i, color in enumerate(colors):
        rect = palette_rects[i]
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        # Highlight selected color
        if color == selected_color:
            pygame.draw.rect(screen, (255, 255, 255), rect, 4)

    text = font.render("Colors", True, (0, 0, 0))
    screen.blit(text, (10, 10))


def draw_tool_info(screen, font, current_tool):
    """Show current tool and controls."""
    lines = [
        f"Tool: {current_tool.upper()}",
        "Keys:",
        "B - Brush",
        "R - Rectangle",
        "C - Circle",
        "E - Eraser",
        "1/2/3/4/5 - Select color",
        "[ / ] - Change brush size"
    ]

    y = 50
    for line in lines:
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (10, y))
        y += 25


def main():
    pygame.init()

    WIDTH, HEIGHT = 1000, 700
    TOOLBAR_HEIGHT = 180

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 22)

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 200, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    GRAY = (200, 200, 200)

    color_list = [BLACK, RED, GREEN, BLUE, YELLOW]
    selected_color = BLACK

    # Canvas surface
    canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
    canvas.fill(WHITE)

    # Tool state
    current_tool = "brush"
    brush_size = 5
    drawing = False
    last_pos = None
    start_pos = None

    # Color palette rectangles
    palette_rects = []
    start_x = 120
    for i in range(len(color_list)):
        rect = pygame.Rect(start_x + i * 60, 10, 40, 40)
        palette_rects.append(rect)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Tool selection
                if event.key == pygame.K_b:
                    current_tool = "brush"
                elif event.key == pygame.K_r:
                    current_tool = "rectangle"
                elif event.key == pygame.K_c:
                    current_tool = "circle"
                elif event.key == pygame.K_e:
                    current_tool = "eraser"

                # Color selection
                elif event.key == pygame.K_1:
                    selected_color = color_list[0]
                elif event.key == pygame.K_2:
                    selected_color = color_list[1]
                elif event.key == pygame.K_3:
                    selected_color = color_list[2]
                elif event.key == pygame.K_4:
                    selected_color = color_list[3]
                elif event.key == pygame.K_5:
                    selected_color = color_list[4]

                # Brush size control
                elif event.key == pygame.K_LEFTBRACKET:
                    brush_size = max(1, brush_size - 1)
                elif event.key == pygame.K_RIGHTBRACKET:
                    brush_size = min(50, brush_size + 1)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # Check palette click
                for i, rect in enumerate(palette_rects):
                    if rect.collidepoint(mx, my):
                        selected_color = color_list[i]

                # Draw only on canvas area
                if my >= TOOLBAR_HEIGHT:
                    drawing = True
                    canvas_pos = (mx, my - TOOLBAR_HEIGHT)
                    start_pos = canvas_pos
                    last_pos = canvas_pos

                    # Start brush/eraser immediately
                    if current_tool == "brush":
                        pygame.draw.circle(canvas, selected_color, canvas_pos, brush_size)
                    elif current_tool == "eraser":
                        pygame.draw.circle(canvas, WHITE, canvas_pos, brush_size)

            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos

                if drawing and my >= TOOLBAR_HEIGHT:
                    canvas_pos = (mx, my - TOOLBAR_HEIGHT)

                    if current_tool == "brush":
                        pygame.draw.line(canvas, selected_color, last_pos, canvas_pos, brush_size * 2)
                        pygame.draw.circle(canvas, selected_color, canvas_pos, brush_size)

                    elif current_tool == "eraser":
                        pygame.draw.line(canvas, WHITE, last_pos, canvas_pos, brush_size * 2)
                        pygame.draw.circle(canvas, WHITE, canvas_pos, brush_size)

                    last_pos = canvas_pos

            elif event.type == pygame.MOUSEBUTTONUP:
                mx, my = event.pos

                if drawing and my >= TOOLBAR_HEIGHT:
                    end_pos = (mx, my - TOOLBAR_HEIGHT)

                    if current_tool == "rectangle":
                        x = min(start_pos[0], end_pos[0])
                        y = min(start_pos[1], end_pos[1])
                        w = abs(end_pos[0] - start_pos[0])
                        h = abs(end_pos[1] - start_pos[1])
                        pygame.draw.rect(canvas, selected_color, (x, y, w, h), 2)

                    elif current_tool == "circle":
                        radius = int(((end_pos[0] - start_pos[0]) ** 2 +
                                      (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                        pygame.draw.circle(canvas, selected_color, start_pos, radius, 2)

                drawing = False
                last_pos = None
                start_pos = None

        # Draw UI
        screen.fill(GRAY)

        # Top toolbar area
        pygame.draw.rect(screen, (230, 230, 230), (0, 0, WIDTH, TOOLBAR_HEIGHT))
        pygame.draw.line(screen, BLACK, (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 2)

        draw_palette(screen, color_list, selected_color, palette_rects, font)
        draw_tool_info(screen, font, current_tool)

        size_text = font.render(f"Brush size: {brush_size}", True, BLACK)
        screen.blit(size_text, (400, 20))

        # Show selected color preview
        pygame.draw.rect(screen, selected_color, (400, 60, 50, 50))
        pygame.draw.rect(screen, BLACK, (400, 60, 50, 50), 2)

        # Draw canvas
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()