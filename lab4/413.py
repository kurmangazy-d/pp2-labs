import json
import sys

def parse_path(path):
    parts = []
    i = 0
    while i < len(path):
        if path[i] == '.':
            i += 1
            continue
        if path[i] == '[':
            i += 1
            j = i
            while j < len(path) and path[j] != ']':
                j += 1
            parts.append(int(path[i:j]))
            i = j + 1
        else:
            j = i
            while j < len(path) and path[j] not in '.[':
                j += 1
            parts.append(path[i:j])
            i = j
    return parts

def resolve(obj, parts):
    cur = obj
    for p in parts:
        if isinstance(p, int):
            if not isinstance(cur, list) or p < 0 or p >= len(cur):
                return False, None
            cur = cur[p]
        else:
            if not isinstance(cur, dict) or p not in cur:
                return False, None
            cur = cur[p]
    return True, cur

data = json.loads(sys.stdin.readline())
q = int(sys.stdin.readline())

for _ in range(q):
    query = sys.stdin.readline().strip()
    parts = parse_path(query)
    found, value = resolve(data, parts)
    if not found:
        print("NOT_FOUND")
    else:
        print(json.dumps(value, separators=(',', ':')))