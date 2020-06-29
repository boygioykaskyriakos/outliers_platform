def shortest_atom(s):
    temp = (s + s).find(s, 1, -1)
    if temp != -1:
        result = s[:temp]
    else:
        result = s

    return result


if __name__ == "__main__":
    assert shortest_atom("ababab") == "ab"
    assert shortest_atom("abcabc") == "abc"
    assert shortest_atom("abcab") == "abcab"

