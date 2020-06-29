from collections import defaultdict

# word = "abcdefghhgfedecba"
# word = "aaaabbcc"
word = "aaaaabc"
dic_normal = defaultdict(int)
dic_inverted = defaultdict(list)
result = ""

for w in word:
    dic_normal[w] += 1

for k, v in dic_normal.items():
    dic_inverted[v].append(k)

if len(dic_inverted.keys()) > 2:
    result = "NO"
elif len(dic_inverted.keys()) == 2:
    values = list(dic_inverted.values())
    keys = list(dic_inverted.keys())

    if len(values[0]) > 1 and len(values[1]) > 1:
        result = "NO"
    elif abs(keys[0] - keys[1]) > 1 and keys[0] > 1 and keys[1] > 1:
        result = "NO"
    elif max(keys)-min(keys) > 1 and len(dic_inverted[max(keys)]) == 1:
        result = "NO"
    else:
        result = "YES"

else:
    result = "YES"

print(result)