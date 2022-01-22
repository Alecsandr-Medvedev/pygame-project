for i in range(50):
    for j in range(50):
        if i == 0 or i == 49 or j == 0 or j == 49:
            a = 1
        else:
            a = 0
        if j == 49:
            b = ''
        else:
            b = ' '
        print(a, end=b)
    print()
