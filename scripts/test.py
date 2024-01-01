from csv import reader
from sys import argv
from pathlib import Path
from datetime import datetime as dt


def get_time(time: str):
    return dt.strptime(time, "%H:%M")


r = list(reader(open(argv[1], "r")))
times = len(r[0])
tolerance = 4 * 60
for i, _ in enumerate(r[2:], start=2):
    l1 = r[i - 1]
    l2 = r[i]
    if len(l1) != times:
        raise Exception(f"Amount Mismatch at {l1}")
    for j in range(times):
        t1 = get_time(l1[j])
        t2 = get_time(l2[j])
        if t2 > t1:
            diff = t2 - t1
        else:
            diff = t1 - t2
        if diff.total_seconds() > tolerance:
            raise Exception(f"Too much diff at {i-1}, {i}: {t1}, {t2}")
