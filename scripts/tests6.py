lines = open('../data/levels/level1/surface3.txt', 'r').readlines()
new_lines = ''
for line in lines:
    new_lines += ' '.join([el for el in line.strip()]) + '\n'

open('../data/levels/level1/surface3.txt', 'w').write(new_lines)
