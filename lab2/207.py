n = int(input())
numbers = list(map(int, input().split()))

maximum = numbers[0]
position = 1  # positions start from 1

for i in range(n):
    if numbers[i] > maximum:
        maximum = numbers[i]
        position = i + 1

print(position)
