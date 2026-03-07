import math

is_prime = lambda n: n > 1 and all(n % i != 0 for i in range(2, int(math.isqrt(n)) + 1))

nums = list(map(int, input().split()))

primes = list(filter(is_prime, nums))

if primes:
    print(*primes)
else:
    print("No primes")
