from collections import defaultdict

dictionary = ["hack", "a", "rank", "khac", "ackh", "kran", "rankhacker", "a", "ab", "ba", "stairs", "raits"]
query = ["a", "nark", "bs", "hack", "stair"]

dictionary_lis = []


dic = {}


def sort_string(word):
    if len(word) > 1:
        return "".join(sorted(word))
    else:
        return word


for element in dictionary:
    element = sort_string(element)
    if element in dic.keys():
        dic[element] += 1
    else:
        dic[element] = 1

for k, v in dic.items():
    print(k, v)

results = []
for q in query:
    q = sort_string(q)
    try:
        results.append(dic[q])
    except KeyError:
        results.append(0)

print(results)

# class HasableDict(dict):
#     def __hash__(self):
#         return hash(tuple(sorted(self.items())))
#
#
# for element in dictionary:
#     dic = defaultdict(lambda: 0)
#
#     for letter in element:
#         dic[letter] += 1
#
#     dictionary_lis.append(dict(dic))
#
# set_of_dicts = set(map(HasableDict, dictionary_lis))
#
# for q in query:
#     dic = defaultdict(lambda: 0)
#
#     for letter in q:
#         dic[letter] += 1
#
#     print(q)
#     if HasableDict(dic) in set_of_dicts:
#         print("true")
#         print(dic)
#     else:
#         print("false")
#         print(dic)

