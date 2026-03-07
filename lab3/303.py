s = input()

digits = {
    "ZER":"0","ONE":"1","TWO":"2","THR":"3","FOU":"4",
    "FIV":"5","SIX":"6","SEV":"7","EIG":"8","NIN":"9"
}
rev = {v:k for k,v in digits.items()}

for op in "+-*":
    if op in s:
        left, right = s.split(op)
        break

def conv(x):
    res = ""
    for i in range(0, len(x), 3):
        res += digits[x[i:i+3]]
    return int(res)

a = conv(left)
b = conv(right)

if op == "+":
    r = a + b
elif op == "-":
    r = a - b
else:
    r = a * b

ans = ""
for d in str(r):
    ans += rev[d]

print(ans)
