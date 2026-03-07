import sys

x1, y1 = map(float, sys.stdin.readline().split())
x2, y2 = map(float, sys.stdin.readline().split())

den = y1 + y2

if abs(den) < 1e-12:
    xr = (x1 + x2) / 2
else:
    t = y1 / den
    xr = x1 + (x2 - x1) * t

print(f"{xr:.10f} 0.0000000000")