n = input()

for d in n:
    if int(d) % 2 == 1:
        print("Not valid")
        break
else:
    print("Valid")
