# Example file showing a basic pygame "game loop"
import pygame
import math
import enum


class Mode(enum.Enum):
    ANIMATE = enum.auto()
    LINE = enum.auto()


class trail_point:
    def __init__(self, vec: pygame.Vector2, lifetime: float) -> None:
        self.v = vec
        self.l = lifetime


# recursive? pogO
def lerp(c: float, start: int, end: int) -> int:
    assert 0 <= c <= 1
    return math.floor(start + c * (end - start))


def lerp2d(c: float, start: pygame.Vector2, end: pygame.Vector2) -> pygame.Vector2:
    x = lerp(c, start.x, end.x)
    y = lerp(c, start.y, end.y)
    return pygame.Vector2(x, y)


def draw_cubic_bez(pts: list, step: float, color: pygame.Color | str) -> None:
    p = 0
    while p <= 1:
        for i in range(len(pts) - 3):
            a = lerp2d(p, pts[i], pts[i + 1])
            b = lerp2d(p, pts[i + 1], pts[i + 2])
            c = lerp2d(p, pts[i + 2], pts[i + 3])

            ab = lerp2d(p, a, b)
            bc = lerp2d(p, b, c)

            pt = lerp2d(p, ab, bc)
            pygame.draw.circle(screen, color, pt, UI_POINT_SIZE)
            p += step


def animate_cubic_bez(pts: list, p: float, color: pygame.Color | str) -> None:
    for i in range(len(pts) - 1):
        pygame.draw.line(screen, UI_LINE_COLOR, pts[i], pts[i + 1], UI_LINE_WIDTH)

    for i in range(len(pts) - 3):

        a = lerp2d(p, pts[i], pts[i + 1])
        b = lerp2d(p, pts[i + 1], pts[i + 2])
        c = lerp2d(p, pts[i + 2], pts[i + 3])

        pygame.draw.line(screen, UI_LINE_COLOR, a, b, UI_LINE_WIDTH)
        pygame.draw.line(screen, UI_LINE_COLOR, b, c, UI_LINE_WIDTH)

        pygame.draw.circle(screen, UI_ACCENT_COLOR, a, UI_POINT_SIZE)
        pygame.draw.circle(screen, UI_ACCENT_COLOR, b, UI_POINT_SIZE)
        pygame.draw.circle(screen, UI_ACCENT_COLOR, c, UI_POINT_SIZE)

        ab = lerp2d(p, a, b)
        bc = lerp2d(p, b, c)

        pygame.draw.line(screen, UI_LINE_COLOR, ab, bc, UI_LINE_WIDTH)

        pygame.draw.circle(screen, UI_ACCENT_COLOR, ab, UI_POINT_SIZE)
        pygame.draw.circle(screen, UI_ACCENT_COLOR, bc, UI_POINT_SIZE)

        pt = lerp2d(p, ab, bc)
        pygame.draw.circle(screen, color, pt, UI_POINT_SIZE)
        if UI_TRAIL_LIFETIME > 0:

            trail.append(trail_point(pt, UI_TRAIL_LIFETIME))


# pygame setup
pygame.init()
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
running = True
mode = Mode.LINE
dragging = False
dragged = -1

dt = 0
t = 0
points = [
    pygame.Vector2(100, 500),
    pygame.Vector2(200, 150),
    pygame.Vector2(400, 500),
    pygame.Vector2(600, 100),
]
trail = []

UI_POINT_SIZE = 8
UI_POINT_COLOR = "purple"
UI_ACCENT_COLOR = "blue"
UI_LINE_COLOR = pygame.Color(100, 100, 100)
UI_LINE_WIDTH = 3
UI_TRAIL_COLOR = "green"
UI_TRAIL_LIFETIME = 0.7
UI_TRAIL_SIZE = 3


while running:
    e = pygame.event.get()
    for event in e:
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    # RENDER YOUR GAME HERE

    for event in e:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                trail = []
                if mode == Mode.LINE:
                    mode = Mode.ANIMATE
                elif mode == Mode.ANIMATE:
                    mode = Mode.LINE

        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, p in enumerate(points):
                m_pos = pygame.Vector2(event.pos)
                distance = m_pos.distance_to(p)
                if distance <= UI_POINT_SIZE:
                    dragging = True
                    dragged = i
                    points[i] = m_pos

    if pygame.mouse.get_pressed()[0]:
        # check for dragging
        if dragging:
            m_pos = pygame.Vector2(pygame.mouse.get_pos())
            points[dragged] = m_pos

    if mode == mode.LINE:
        draw_cubic_bez(points, 0.05, UI_ACCENT_COLOR)
    elif mode == mode.ANIMATE:
        c = 0.5 * (math.sin(t) + 1)
        animate_cubic_bez(points, c, "green")

    for i, p in enumerate(trail):
        if p.l <= 0:
            trail.pop(i)
        else:
            pygame.draw.circle(screen, UI_TRAIL_COLOR, p.v, UI_TRAIL_SIZE)
            p.l -= dt

    for p in points:
        pygame.draw.circle(screen, UI_POINT_COLOR, p, UI_POINT_SIZE)

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000  # limits FPS to 60
    t += dt

pygame.quit()
