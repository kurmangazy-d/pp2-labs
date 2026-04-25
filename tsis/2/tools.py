import pygame
from collections import deque


def draw_palette(screen, colors, selected_color, palette_rects, font):
    title = font.render("Colors:", True, (0, 0, 0))
    screen.blit(title, (10, 10))

    for i, color in enumerate(colors):
        rect = palette_rects[i]
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        if color == selected_color:
            pygame.draw.rect(screen, (255, 255, 255), rect, 4)


def draw_size_buttons(screen, size_rects, brush_size, font):
    title = font.render("Brush Size:", True, (0, 0, 0))
    screen.blit(title, (10, 68))

    labels = ["1 Small", "2 Medium", "3 Large"]
    values = [2, 5, 10]

    for i, rect in enumerate(size_rects):
        pygame.draw.rect(screen, (220, 220, 220), rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        if brush_size == values[i]:
            pygame.draw.rect(screen, (255, 255, 255), rect, 4)

        text = font.render(labels[i], True, (0, 0, 0))
        screen.blit(text, (rect.x + 12, rect.y + 10))


def draw_tool_buttons(screen, tool_rects, current_tool, font):
    title = font.render("Tools:", True, (0, 0, 0))
    screen.blit(title, (10, 128))

    tool_names = [
        "brush", "line", "rectangle", "circle",
        "eraser", "square", "right_triangle", "equilateral_triangle",
        "rhombus", "fill", "text"
    ]

    tool_labels = [
        "B Brush", "L Line", "R Rect", "C Circle",
        "E Erase", "S Square", "T RightTri", "Q EquiTri",
        "H Rhombus", "F Fill", "X Text"
    ]

    for i, rect in enumerate(tool_rects):
        pygame.draw.rect(screen, (220, 220, 220), rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        if current_tool == tool_names[i]:
            pygame.draw.rect(screen, (255, 255, 255), rect, 4)

        text = font.render(tool_labels[i], True, (0, 0, 0))
        screen.blit(text, (rect.x + 8, rect.y + 8))


def draw_status(screen, font, current_tool, brush_size):
    lines = [
        f"Current tool: {current_tool}",
        f"Brush size: {brush_size}",
        "Ctrl+S -> Save canvas",
        "Enter -> Confirm text",
        "Esc -> Cancel text"
    ]

    y = 250
    for line in lines:
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (10, y))
        y += 22


def flood_fill(surface, x, y, fill_color):
    width, height = surface.get_size()

    if not (0 <= x < width and 0 <= y < height):
        return

    target_color = surface.get_at((x, y))
    fill_color_rgba = pygame.Color(*fill_color, 255)

    if target_color == fill_color_rgba:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        px, py = queue.popleft()

        if not (0 <= px < width and 0 <= py < height):
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), fill_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))