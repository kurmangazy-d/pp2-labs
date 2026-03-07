import sys
import math

r = float(sys.stdin.readline())
x1, y1 = map(float, sys.stdin.readline().split())
x2, y2 = map(float, sys.stdin.readline().split())

dx = x2 - x1
dy = y2 - y1

A = dx*dx + dy*dy
B = 2*(x1*dx + y1*dy)
C = x1*x1 + y1*y1 - r*r

D = B*B - 4*A*C

if A == 0 or D <= 0:
    print("0.0000000000")
    sys.exit()

sqrtD = math.sqrt(D)
t1 = (-B - sqrtD) / (2*A)
t2 = (-B + sqrtD) / (2*A)
lo = max(0, min(t1, t2))
hi = min(1, max(t1, t2))

if lo > hi:
    print("0.0000000000")
else:
    length = math.hypot(dx, dy) * (hi - lo)
    print(f"{length:.10f}")