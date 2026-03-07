import sys
import importlib

n = int(sys.stdin.readline())

for _ in range(n):
    line = sys.stdin.readline().rstrip()
    if not line:
        print("ATTRIBUTE_NOT_FOUND")
        continue
    module_path, attr = line.split()

    try:
        module = importlib.import_module(module_path)
    except ImportError:
        print("MODULE_NOT_FOUND")
        continue

    if not hasattr(module, attr):
        print("ATTRIBUTE_NOT_FOUND")
        continue

    value = getattr(module, attr)
    print("CALLABLE" if callable(value) else "VALUE")