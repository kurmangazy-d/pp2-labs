import re
a=input()
res=re.findall(r'[A-Z]',a)
print(len(res))