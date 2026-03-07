def divisible_by_12(n):
    for i in range(0, n + 1):
        if i % 12 == 0:
            yield i

n = int(input())

for num in divisible_by_12(n):
    print(num, end=" ")