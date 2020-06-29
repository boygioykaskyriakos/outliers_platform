
words = [
    "AAAA",
    "BBBBB",
    "ABABABAB",
    "BABABA",
    "AAABBB"
]


for word in words:
    counter = 0
    i = 0
    while True:
        if i+1 >= len(word):
            break
        elif word[i] == word[i+1]:
            word = word[:i+1] + word[i+2:]
            counter += 1
        else:
            i += 1
    print(counter)

