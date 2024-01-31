from sys import argv
import re
from csv import writer

f = open(argv[1], "r")
lines = f.readlines()
of = open(argv[2], "w")
print(len(lines))
w = writer(of)
for i in range(len(lines) // 6):
    line = lines[6 * i : 6 * (i + 1)]
    line = [x.strip() for x in line]
    w.writerow(line)

of.close()
