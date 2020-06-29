import math
from collections import deque

# skillLevel = [3, 4, 5, 2, 1, 1]
# skillLevel = [1, 2, 3, 4, 5,6]

# minDiff = 3



skillLevel = [
    709552565, 473251358, 803612259, 579542802, 183012194, 689345248,
    151290765, 123232501, 994391793, 25107191, 862726097
]
minDiff = 22586934

dic = {}
pairs = 0


# print(skillLevel)
#
# i = 0
# while i < len(skillLevel):
#     k = 1
#     while i+k < len(skillLevel):
#         print(skillLevel[i], skillLevel[i+k])
#         if abs(skillLevel[i] - skillLevel[i+k]) >= minDiff:
#             print("found {}, {}".format(skillLevel[i], skillLevel[i+k]))
#             pairs += 1
#             skillLevel.pop(i + k)
#             skillLevel.pop(i)
#             print("new skillLevel {}".format(skillLevel))
#             i -= 1
#             break
#
#         k += 1
#     i += 1
#
#
# print(pairs)

