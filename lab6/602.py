a=int(input())
n=list(map(int, input().split()))
even=list(filter(lambda x: x%2==0, n))
print(len(even))