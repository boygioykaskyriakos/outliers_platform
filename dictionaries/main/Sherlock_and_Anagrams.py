# find smallest lenght of subarray that reflects the target
lis = [[1, 2, 3, 4], 6]


def check_by_removing_last(lis, target, solutions):
    if sum(lis[1:]) >= target:
        lis.pop(0)
        solutions.append(lis)

        return check_by_removing_last(lis, target, solutions)
    else:
        return solutions


def find_least(arr, target):
    solutions = []
    lis = []
    for a in arr:
        lis.append(a)

        if sum(lis) >= target:
            solutions.append(lis)
            solutions = check_by_removing_last(lis, target, solutions)

    res = min(map(len, solutions))

    for s in solutions:
        if len(s) == res:
            return s


res = find_least([1,2,3,4], 6)
print(res)


