lis = [1, 2, 3, 4, 5]
target = lis[0]
arr = [lis[0]]


def calc_target(arr, target):
    temp_target = len(arr) * min(arr)

    if temp_target > target:
        target = temp_target

    return target


def check_backwards(arr, target):
    arr.pop(0)
    target = calc_target(arr, target)

    return target


for l in lis[1:]:
    arr.append(l)

    target = calc_target(arr, target)

