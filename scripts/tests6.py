def func1(a):
    return a


def func2(a):
    return a - 1


for i in range(1, 3):
    b = i * 2
    a = eval(f'func{i}(b)')
    print(a)