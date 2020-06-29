# find smallest lenght of subarray that reflects the target
lis = [[1, 2, 3, 4], 6]


def check_by_removing_last(lis, target, solutions):
    temp_lis = lis.copy()
    if sum(lis[1:]) >= target:
        temp_lis.pop(0)
        solutions.append(temp_lis)

        return check_by_removing_last(temp_lis, target, solutions)
    else:
        return solutions


def find_least(arr, target):
    solutions = []
    lis = []
    for a in arr:
        lis.append(a)

        if sum(lis) >= target:
            solution = lis.copy()
            solutions.append(solution)
            solutions = check_by_removing_last(solution, target, solutions)
            lis = solutions[-1].copy()

    res = min(map(len, solutions))

    print(solutions)
    return res


res = find_least([1, 2, 3, 4, 2, 5, 6], 6)
print(res)


