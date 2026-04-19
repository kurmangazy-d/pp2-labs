import pygame
import math

# ---------------------------------
# Paint Program with:
# - Brush
# - Rectangle
# - Circle
# - Eraser
# - Color selection
# - Square
# - Right triangle
# - Equilateral triangle
# - Rhombus
# ---------------------------------


def draw_palette(screen, colors, selected_color, palette_rects, font):
    for i, color in enumerate(colors):
        rect = palette_rects[i]
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        
        if color == selected_color:
            pygame.draw.rect(screen, (255, 255, 255), rect, 4)

    text = font.render("Colors", True, (0, 0, 0))
    screen.blit(text, (10, 10))


def draw_tool_info(screen, font, current_tool, brush_size):
    left_lines = [
        f"Tool: {current_tool.upper()}",
        "B - Brush",
        "R - Rectangle",
        "C - Circle",
        "E - Eraser",
        "S - Square"
    ]

    right_lines = [
        "T - Right triangle",
        "Q - Equilateral triangle",
        "H - Rhombus",
        "1/2/3/4/5 - Color",
        "[ / ] - Brush size",
        f"Size: {brush_size}"
    ]

    y = 55
    for line in left_lines:
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (10, y))
        y += 22

    y = 55
    for line in right_lines:
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (260, y))
        y += 22


def main():
    pygame.init()

    WIDTH, HEIGHT = 1000, 700
    TOOLBAR_HEIGHT = 210   

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    #цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 200, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    GRAY = (200, 200, 200)

    color_list = [BLACK, RED, GREEN, BLUE, YELLOW]
    selected_color = BLACK

    #канва
    canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
    canvas.fill(WHITE)

    #настройки
    current_tool = "brush"
    brush_size = 5
    drawing = False
    last_pos = None
    start_pos = None

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
                if event.key == pygame.K_b:
                    current_tool = "brush"
                elif event.key == pygame.K_r:
                    current_tool = "rectangle"
                elif event.key == pygame.K_c:
                    current_tool = "circle"
                elif event.key == pygame.K_e:
                    current_tool = "eraser"
                elif event.key == pygame.K_s:
                    current_tool = "square"
                elif event.key == pygame.K_t:
                    current_tool = "right_triangle"
                elif event.key == pygame.K_q:
                    current_tool = "equilateral_triangle"
                elif event.key == pygame.K_h:
                    current_tool = "rhombus"

                #выбираем цвет
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

                #меняем кисточку размер
                elif event.key == pygame.K_LEFTBRACKET:
                    brush_size = max(1, brush_size - 1)
                elif event.key == pygame.K_RIGHTBRACKET:
                    brush_size = min(50, brush_size + 1)

        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

               
                for i, rect in enumerate(palette_rects):
                    if rect.collidepoint(mx, my):
                        selected_color = color_list[i]

                
                if my >= TOOLBAR_HEIGHT:
                    drawing = True
                    canvas_pos = (mx, my - TOOLBAR_HEIGHT)
                    start_pos = canvas_pos
                    last_pos = canvas_pos

                    
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

                    x1, y1 = start_pos
                    x2, y2 = end_pos

                    
                    if current_tool == "rectangle":
                        x = min(x1, x2)
                        y = min(y1, y2)
                        w = abs(x2 - x1)
                        h = abs(y2 - y1)
                        pygame.draw.rect(canvas, selected_color, (x, y, w, h), 2)

                    
                    elif current_tool == "circle":
                        radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                        pygame.draw.circle(canvas, selected_color, start_pos, radius, 2)

                    
                    elif current_tool == "square":
                        side = min(abs(x2 - x1), abs(y2 - y1))

                        
                        if x2 >= x1:
                            x = x1
                        else:
                            x = x1 - side

                        if y2 >= y1:
                            y = y1
                        else:
                            y = y1 - side

                        pygame.draw.rect(canvas, selected_color, (x, y, side, side), 2)

                    
                    elif current_tool == "right_triangle":
                        points = [
                            (x1, y1),
                            (x1, y2),
                            (x2, y2)
                        ]
                        pygame.draw.polygon(canvas, selected_color, points, 2)

                    
                    elif current_tool == "equilateral_triangle":
                        side = abs(x2 - x1)

                        
                        if x2 < x1:
                            side = -side

                        height = abs(side) * math.sqrt(3) / 2

                        
                        if y2 >= y1:
                            top_y = y1 + height
                        else:
                            top_y = y1 - height

                        points = [
                            (x1, y1),
                            (x1 + side, y1),
                            (x1 + side / 2, top_y)
                        ]
                        pygame.draw.polygon(canvas, selected_color, points, 2)

                    
                    elif current_tool == "rhombus":
                        center_x = (x1 + x2) / 2
                        center_y = (y1 + y2) / 2

                        points = [
                            (center_x, y1),   # top
                            (x2, center_y),   # right
                            (center_x, y2),   # bottom
                            (x1, center_y)    # left
                        ]
                        pygame.draw.polygon(canvas, selected_color, points, 2)

                drawing = False
                last_pos = None
                start_pos = None

        
        screen.fill(GRAY)

        
        pygame.draw.rect(screen, (230, 230, 230), (0, 0, WIDTH, TOOLBAR_HEIGHT))
        pygame.draw.line(screen, BLACK, (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 2)

        draw_palette(screen, color_list, selected_color, palette_rects, font)
        draw_tool_info(screen, font, current_tool, brush_size)

        
        preview_text = font.render("Selected:", True, BLACK)
        screen.blit(preview_text, (520, 15))
        pygame.draw.rect(screen, selected_color, (600, 10, 45, 45))
        pygame.draw.rect(screen, BLACK, (600, 10, 45, 45), 2)

        
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()