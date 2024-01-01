from sys import argv
import re
from csv import writer

pattern = re.compile("\d{1,2}.\d\d")
f = open(argv[1], "r")
lines = []
line = []
for l in f.readlines():
    t = pattern.findall(l)
    if not t:
        continue
    for x in t:
        line.append(x)
        if len(line) == 5:
            lines.append(line)
            line = []

of = open(argv[2], "w")
w = writer(of)
w.writerows(lines)
of.close()
