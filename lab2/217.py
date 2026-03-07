n = int(input())
counts = {}

for _ in range(n):
    number = input()
    if number in counts:
        counts[number] += 1
    else:
        counts[number] = 1

result = 0
for num in counts:
    if counts[num] == 3:
        result += 1

print(result)
