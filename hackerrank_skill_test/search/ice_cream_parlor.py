pair = 2
# target = 5
target = 4
size_of_array = 5
# lis = [1, 4, 5, 3, 2]
# lis = [4, 3, 2, 5, 7]
lis = [2, 2, 4, 3]


def find_comb(cost, money):
    array = cost.copy()
    array.sort()
    i = 0
    j = len(array)-1

    while i < j:
        target_sum = array[i] + array[j]

        if target_sum == money:
            break
        elif target_sum < money:
            i += 1
        else:
            j -= 1

    left = array[i]
    right = array[j]

    if left == right:
        res = [idc for idc, x in enumerate(cost) if x==left]
        idx_cost_left = res[0]
        idx_cost_right = res[1]

    else:
        idx_cost_left = cost.index(left)
        idx_cost_right = cost.index(right)

    if idx_cost_left < idx_cost_right:
        print(idx_cost_left, idx_cost_right)
    else:
        print(idx_cost_right, idx_cost_left)





find_comb(lis, target)
