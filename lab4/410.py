def cycle(lst, times):
    for _ in range(times):
        for item in lst:
            yield item

elements = input().split()
n = int(input())

print(" ".join(cycle(elements, n)))