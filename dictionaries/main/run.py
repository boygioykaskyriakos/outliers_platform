import time
import csv

from collections import defaultdict


def time_count(func):
    def wrapper(arg):
        start_time = time.time()
        func(arg)
        end_time = time.time()-start_time
        return arg+end_time

    return wrapper


if __name__ == "__main__":
    dic = defaultdict(lambda: 0)
    dic_2 = defaultdict(lambda: 0)
    res = []
    queries = []

    time_1 = 0
    time_2 = 0
    time_3 = 0

    with open("input11.txt", "r") as tsv:
        for line in csv.reader(tsv, delimiter="\t"):
            queries.append(line[0].split())

    @time_count
    def func_1(arg):
        dic[b] += 1
        dic_2[dic[b]] += 1

        return arg

    @time_count
    def func_2(arg):
        if b in dic.keys():
            if dic[b] > 0:
                dic[b] -= 1
                dic_2[dic[b]] -= 1

        return arg

    @time_count
    def func_3(arg):
        x = 1 if dic_2[b] > 0 else 0
        res.append(x)

        return arg

    for q in queries:
        a = int(q[0])
        b = int(q[1])

        if a == 1:
            time_1 = func_1(time_1)
        elif a == 2:
            time_2 = func_2(time_2)
        else:
            time_3 = func_3(time_3)

    print(time_1)
    print(time_2)
    print(time_3)
    # print(res)

"""
d = defaultdict(int) ; f = defaultdict(set)

    for (c,v) in queries:
        if c==3 : yield int( len(f[v])>0 ) ; continue

        f[d[v]].discard(v)
        if c==1 : d[v] += 1
        elif d[v]>0 : d[v] -= 1
        f[d[v]].add(v)
"""