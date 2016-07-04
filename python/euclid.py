def euclid(x, y):
    if x < y:
        x, y = y, x
    r = x % y
    if r == 0:
        print("gcd = " + str(y))
    else:
        euclid(y, r)

print("Input two integer:")

a = int(input())
b = int(input())

euclid(a, b)
