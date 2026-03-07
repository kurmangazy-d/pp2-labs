import json
import sys

def apply_patch(src, patch):
    for key, value in patch.items():
        if value is None:
            src.pop(key, None)
        elif isinstance(value, dict) and isinstance(src.get(key), dict):
            apply_patch(src[key], value)
        else:
            src[key] = value
    return src

source = json.loads(sys.stdin.readline())
patch = json.loads(sys.stdin.readline())

result = apply_patch(source, patch)

print(json.dumps(result, sort_keys=True, separators=(',', ':')))