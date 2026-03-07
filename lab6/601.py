a=int(input())
n=list(map(int,input().split()))
squares=map(lambda x: x**2, n)
print(sum(squares))