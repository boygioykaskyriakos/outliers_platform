from collections import defaultdict, deque

word = "abcbaba"
d = deque()
counter = 0

for w in word:
    d.append(w)

    if len(d) > 1:
        s0 = d[0]
        if all(c == s0 for c in d[1:]):
            counter += 1


