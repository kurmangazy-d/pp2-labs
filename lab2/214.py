n = int(input())
arr = list(map(int, input().split()))

freq = {}
for num in arr:
    if num in freq:
        freq[num] += 1
    else:
        freq[num] = 1

max_count = 0
most_frequent = None
for num in freq:
    if freq[num] > max_count or (freq[num] == max_count and num < most_frequent):
        max_count = freq[num]
        most_frequent = num

print(most_frequent)
