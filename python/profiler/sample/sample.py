def f1(n):
    counter = 0
    for i in range(n):
        counter += 1
    return counter

def f2(n):
    counter = 0
    for j in range(n):
        f1(n)
    return counter

def f3(n):
    counter = 0
    for k in range(n):
        f2(n)
    return counter

f1(500)
f2(500)
f3(500)
