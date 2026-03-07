import json
import sys

def diff(a, b, path, diffs):
    keys = set(a.keys()) | set(b.keys())
    for key in keys:
        new_path = f"{path}.{key}" if path else key
        in_a = key in a
        in_b = key in b

        if not in_a:
            diffs.append((new_path, "<missing>", json.dumps(b[key], separators=(',', ':'))))
        elif not in_b:
            diffs.append((new_path, json.dumps(a[key], separators=(',', ':')), "<missing>"))
        else:
            va, vb = a[key], b[key]
            if isinstance(va, dict) and isinstance(vb, dict):
                diff(va, vb, new_path, diffs)
            elif va != vb:
                diffs.append((new_path,
                              json.dumps(va, separators=(',', ':')),
                              json.dumps(vb, separators=(',', ':'))))

source = json.loads(sys.stdin.readline())
target = json.loads(sys.stdin.readline())

diffs = []
diff(source, target, "", diffs)

if not diffs:
    print("No differences")
else:
    for path, old, new in sorted(diffs, key=lambda x: x[0]):
        print(f"{path} : {old} -> {new}")