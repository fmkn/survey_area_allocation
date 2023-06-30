# -*- coding: utf-8 -*-
with open('groups.txt', 'r') as f:
    lines = f.readlines()

output = []
for line in lines:
    line = line.strip().split(',')
    group_number = line[0]
    for i in range(-3, 0):
        row_number = int(line[i])
        while len(output) < row_number:
            output.append('')
        output[row_number - 1] = group_number

with open('line_group.txt', 'w') as f:
    for line in output:
        f.write(line + '\n')
