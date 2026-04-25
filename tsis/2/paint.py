import pygame
import math
from datetime import datetime
from tools import (
    draw_palette,
    draw_size_buttons,
    draw_tool_buttons,
    draw_status,
    flood_fill
)


def main():
    pygame.init()

    WIDTH, HEIGHT = 1200, 850
    TOOLBAR_HEIGHT = 340
    CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS 2 Paint")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 14)
    text_font = pygame.font.SysFont("Arial", 24)

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 180, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (160, 32, 240)
    ORANGE = (255, 140, 0)
    GRAY = (200, 200, 200)
    LIGHT_GRAY = (230, 230, 230)

    color_list = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE]
    selected_color = BLACK

    # Canvas
    canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
    canvas.fill(WHITE)

    # State
    current_tool = "brush"
    brush_size = 5
    drawing = False
    start_pos = None
    last_pos = None
    current_mouse_canvas = None

    # Text tool state
    text_mode = False
    text_position = None
    current_text = ""

    # Color buttons
    palette_rects = []
    for i in range(len(color_list)):
        palette_rects.append(pygame.Rect(110 + i * 55, 10, 40, 40))

    # Brush size buttons
    size_rects = [
        pygame.Rect(110, 60, 100, 35),
        pygame.Rect(220, 60, 110, 35),
        pygame.Rect(340, 60, 100, 35)
    ]

    # Tool buttons
    tool_rects = []
    tool_start_x = 110
    tool_start_y = 120
    tool_w = 150
    tool_h = 32
    gap_x = 10
    gap_y = 8

    tool_names = [
        "brush", "line", "rectangle", "circle",
        "eraser", "square", "right_triangle", "equilateral_triangle",
        "rhombus", "fill", "text"
    ]

    for i in range(len(tool_names)):
        row = i // 4
        col = i % 4
        rect = pygame.Rect(
            tool_start_x + col * (tool_w + gap_x),
            tool_start_y + row * (tool_h + gap_y),
            tool_w,
            tool_h
        )
        tool_rects.append(rect)

    running = True
    while running:
        preview_surface = canvas.copy()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # ---------------- KEYDOWN ----------------
            elif event.type == pygame.KEYDOWN:
                # Save canvas with Ctrl+S
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"paint_{timestamp}.png"
                    pygame.image.save(canvas, filename)
                    print(f"Saved: {filename}")

                # Text typing mode
                elif text_mode:
                    if event.key == pygame.K_RETURN:
                        if current_text.strip() != "":
                            rendered = text_font.render(current_text, True, selected_color)
                            canvas.blit(rendered, text_position)
                        text_mode = False
                        current_text = ""
                        text_position = None

                    elif event.key == pygame.K_ESCAPE:
                        text_mode = False
                        current_text = ""
                        text_position = None

                    elif event.key == pygame.K_BACKSPACE:
                        current_text = current_text[:-1]

                    else:
                        if event.unicode.isprintable():
                            current_text += event.unicode

                else:
                    # Tool shortcuts
                    if event.key == pygame.K_b:
                        current_tool = "brush"
                    elif event.key == pygame.K_l:
                        current_tool = "line"
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
                    elif event.key == pygame.K_f:
                        current_tool = "fill"
                    elif event.key == pygame.K_x:
                        current_tool = "text"

                    # Brush size shortcuts
                    elif event.key == pygame.K_1:
                        brush_size = 2
                    elif event.key == pygame.K_2:
                        brush_size = 5
                    elif event.key == pygame.K_3:
                        brush_size = 10

            # ---------------- MOUSE DOWN ----------------
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # Color selection
                for i, rect in enumerate(palette_rects):
                    if rect.collidepoint(mx, my):
                        selected_color = color_list[i]

                # Brush size buttons
                if size_rects[0].collidepoint(mx, my):
                    brush_size = 2
                elif size_rects[1].collidepoint(mx, my):
                    brush_size = 5
                elif size_rects[2].collidepoint(mx, my):
                    brush_size = 10

                # Tool buttons
                for i, rect in enumerate(tool_rects):
                    if rect.collidepoint(mx, my):
                        current_tool = tool_names[i]

                # Canvas click
                if my >= TOOLBAR_HEIGHT:
                    canvas_pos = (mx, my - TOOLBAR_HEIGHT)

                    if current_tool == "fill":
                        flood_fill(canvas, canvas_pos[0], canvas_pos[1], selected_color)

                    elif current_tool == "text":
                        text_mode = True
                        text_position = canvas_pos
                        current_text = ""

                    else:
                        drawing = True
                        start_pos = canvas_pos
                        last_pos = canvas_pos
                        current_mouse_canvas = canvas_pos

                        if current_tool == "brush":
                            pygame.draw.circle(canvas, selected_color, canvas_pos, brush_size)

                        elif current_tool == "eraser":
                            pygame.draw.circle(canvas, WHITE, canvas_pos, brush_size)

            # ---------------- MOUSE MOTION ----------------
            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos

                if my >= TOOLBAR_HEIGHT:
                    current_mouse_canvas = (mx, my - TOOLBAR_HEIGHT)

                if drawing and my >= TOOLBAR_HEIGHT:
                    canvas_pos = (mx, my - TOOLBAR_HEIGHT)
                    current_mouse_canvas = canvas_pos

                    if current_tool == "brush":
                        pygame.draw.line(canvas, selected_color, last_pos, canvas_pos, brush_size)
                        pygame.draw.circle(canvas, selected_color, canvas_pos, brush_size)

                    elif current_tool == "eraser":
                        pygame.draw.line(canvas, WHITE, last_pos, canvas_pos, brush_size)
                        pygame.draw.circle(canvas, WHITE, canvas_pos, brush_size)

                    last_pos = canvas_pos

            # ---------------- MOUSE UP ----------------
            elif event.type == pygame.MOUSEBUTTONUP:
                mx, my = event.pos

                if drawing and my >= TOOLBAR_HEIGHT:
                    end_pos = (mx, my - TOOLBAR_HEIGHT)

                    x1, y1 = start_pos
                    x2, y2 = end_pos

                    if current_tool == "line":
                        pygame.draw.line(canvas, selected_color, start_pos, end_pos, brush_size)

                    elif current_tool == "rectangle":
                        x = min(x1, x2)
                        y = min(y1, y2)
                        w = abs(x2 - x1)
                        h = abs(y2 - y1)
                        pygame.draw.rect(canvas, selected_color, (x, y, w, h), brush_size)

                    elif current_tool == "circle":
                        radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
                        pygame.draw.circle(canvas, selected_color, start_pos, radius, brush_size)

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

                        pygame.draw.rect(canvas, selected_color, (x, y, side, side), brush_size)

                    elif current_tool == "right_triangle":
                        points = [(x1, y1), (x1, y2), (x2, y2)]
                        pygame.draw.polygon(canvas, selected_color, points, brush_size)

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
                        pygame.draw.polygon(canvas, selected_color, points, brush_size)

                    elif current_tool == "rhombus":
                        center_x = (x1 + x2) / 2
                        center_y = (y1 + y2) / 2
                        points = [
                            (center_x, y1),
                            (x2, center_y),
                            (center_x, y2),
                            (x1, center_y)
                        ]
                        pygame.draw.polygon(canvas, selected_color, points, brush_size)

                drawing = False
                start_pos = None
                last_pos = None

        # ---------------- PREVIEW FOR SHAPES ----------------
        if drawing and start_pos and current_mouse_canvas:
            x1, y1 = start_pos
            x2, y2 = current_mouse_canvas

            if current_tool == "line":
                pygame.draw.line(preview_surface, selected_color, start_pos, current_mouse_canvas, brush_size)

            elif current_tool == "rectangle":
                x = min(x1, x2)
                y = min(y1, y2)
                w = abs(x2 - x1)
                h = abs(y2 - y1)
                pygame.draw.rect(preview_surface, selected_color, (x, y, w, h), brush_size)

            elif current_tool == "circle":
                radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
                pygame.draw.circle(preview_surface, selected_color, start_pos, radius, brush_size)

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

                pygame.draw.rect(preview_surface, selected_color, (x, y, side, side), brush_size)

            elif current_tool == "right_triangle":
                points = [(x1, y1), (x1, y2), (x2, y2)]
                pygame.draw.polygon(preview_surface, selected_color, points, brush_size)

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
                pygame.draw.polygon(preview_surface, selected_color, points, brush_size)

            elif current_tool == "rhombus":
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                points = [
                    (center_x, y1),
                    (x2, center_y),
                    (center_x, y2),
                    (x1, center_y)
                ]
                pygame.draw.polygon(preview_surface, selected_color, points, brush_size)

        # ---------------- DRAW UI ----------------
        screen.fill(GRAY)
        pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
        pygame.draw.line(screen, BLACK, (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 2)

        draw_palette(screen, color_list, selected_color, palette_rects, font)
        draw_size_buttons(screen, size_rects, brush_size, font)
        draw_tool_buttons(screen, tool_rects, current_tool, font)
        draw_status(screen, font, current_tool, brush_size)

        # Selected color preview
        preview_text = font.render("Selected Color:", True, BLACK)
        screen.blit(preview_text, (850, 20))
        pygame.draw.rect(screen, selected_color, (980, 15, 50, 50))
        pygame.draw.rect(screen, BLACK, (980, 15, 50, 50), 2)

        # Draw preview/canvas
        if drawing and current_tool in [
            "line", "rectangle", "circle", "square",
            "right_triangle", "equilateral_triangle", "rhombus"
        ]:
            screen.blit(preview_surface, (0, TOOLBAR_HEIGHT))
        else:
            screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        # Draw text preview while typing
        if text_mode and text_position:
            preview_text_surface = text_font.render(current_text + "|", True, selected_color)
            screen.blit(preview_text_surface, (text_position[0], text_position[1] + TOOLBAR_HEIGHT))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()