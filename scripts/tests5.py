import os.path

f = os.path.abspath('')
print(f[:-7] + os.path.join('data', 'img', 'Wall.png'))