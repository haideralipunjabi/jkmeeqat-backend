import csv
from sys import argv
from datetime import time

reader = csv.reader(open(argv[1], "r"))
writer = csv.writer(open(argv[2], "w"))
header = []
am = ["fajr", "sunrise", "noon", "zuhr"]
pm = ["maghrib", "isha", "asr"]
for i, row in enumerate(reader):
    if i == 0:
        header = row
        writer.writerow(row)
        continue
    out = []
    for j, item in enumerate(row):
        key = header[j]
        if key in am:
            out.append(item)
            continue
        if key in pm:
            hour, minute = item.split(":")
            hour = int(hour) + 12
            out.append(f"{hour}:{minute}")
    writer.writerow(out)
