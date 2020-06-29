# min operations

"""

arr of integers
minimum number of desired equal elements
the division parameter

arr = [64, 30, 25, 33]
threshold = 2
division parameter = 2

result is 2 64/2 and 33/2
"""


def check_if_duplicates(list_of_elements):
    for elem in list_of_elements:
        if list_of_elements.count(elem) > 1:
            return True
    return False


arr = [64, 30, 25, 33]
threshold = 2
d = 2
match = 0
found = 0
stop = False

i = 1
while True:
    arr += [int((x-1)/d) if x % 2 != 0 and x-1 > 0 else int(x/d) for x in arr]
    if check_if_duplicates(arr):
        print(i)
        break
    else:
        i += 1






