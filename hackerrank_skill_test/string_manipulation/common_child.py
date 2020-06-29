rows = "OUDFRMYMAW"
columns = "AWHYFCCMQX"
max_value = 0


# def lcs(X, Y, m, n):
#     if m == 0 or n == 0:
#         return 0;
#     elif X[m - 1] == Y[n - 1]:
#         return 1 + lcs(X, Y, m - 1, n - 1);
#     else:
#         return max(lcs(X, Y, m, n - 1), lcs(X, Y, m - 1, n));
#
#
# result = lcs(rows, columns, len(rows), len(columns))
# print(result)


arr = [0] * (len(rows)+1)
for r in range(len(rows)+1):
    arr[r] = [0]*len(columns)

for i in range(len(rows)):
    for j in range(len(columns)):
        if i == 0 or j == 0:
            arr[i][j] = 0
        elif rows[i-1] == columns[j-1]:
            arr[i][j] = arr[i-1][j-1] + 1
        else:
            arr[i][j] = max(arr[i][j-1], arr[i-1][j])

        if arr[i][j] > max_value:
            max_value = arr[i][j]

for a in arr:
    print(a)

print(max_value)







