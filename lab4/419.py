import sys
import math

def dist_point_segment(cx, cy, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(cx - x1, cy - y1)
    t = ((cx - x1) * dx + (cy - y1) * dy) / (dx * dx + dy * dy)
    t = max(0, min(1, t))
    px = x1 + t * dx
    py = y1 + t * dy
    return math.hypot(cx - px, cy - py)

def shortest_around_circle(r, x1, y1, x2, y2):
    da = math.hypot(x1, y1)
    db = math.hypot(x2, y2)

    ta = math.sqrt(da*da - r*r)
    tb = math.sqrt(db*db - r*r)

    alpha = math.atan2(y1, x1)
    beta = math.atan2(y2, x2)
    thetaA = math.acos(r / da)
    thetaB = math.acos(r / db)

    best = float('inf')
    for pa in (alpha + thetaA, alpha - thetaA):
        for pb in (beta + thetaB, beta - thetaB):
            diff = abs(pa - pb)
            arc = min(diff, 2*math.pi - diff)
            best = min(best, ta + tb + r * arc)
    return best

r = float(sys.stdin.readline())
x1, y1 = map(float, sys.stdin.readline().split())
x2, y2 = map(float, sys.stdin.readline().split())

if dist_point_segment(0, 0, x1, y1, x2, y2) >= r - 1e-9:
    ans = math.hypot(x2 - x1, y2 - y1)
else:
    ans = shortest_around_circle(r, x1, y1, x2, y2)

print(f"{ans:.10f}")