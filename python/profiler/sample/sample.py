def f1(n):
    counter = 0
    for i in range(n):
        counter += 1
    return counter

def f2(n):
    counter = 0
    for i in range(n):
        for j in range(n):
            counter += 1
    return counter

def f3(n):
    counter = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                counter += 1
    return counter

f1(1000)
f2(1000)
f3(1000)
