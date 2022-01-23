a = 8
b = [1, 2, 3, 4, 5, 6, 7, 8]
c = 0
while True:
    c = (c + 1) % a
    print(b[c])