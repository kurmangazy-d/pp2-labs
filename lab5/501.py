import re

a=input()
res=re.match(r"Hello", a)
if res:
    print("Yes")
else:
    print("No")