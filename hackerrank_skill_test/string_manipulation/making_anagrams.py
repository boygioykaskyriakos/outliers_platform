import string

# a = "cde"
# b = "abc"
a = "fcrxzwscanmligyxyvym"
b = "jxwtrhvujlmrpdoqbisbwhmgpmeoke"

a = "".join(sorted(a))
b = "".join(sorted(b))
counter = 0


for l in string.ascii_lowercase:
    if a == b:
        break
    else:
        if l in a and l in b:
            a_count_l = a.count(l)
            b_count_l = b.count(l)

            if a_count_l == b_count_l:
                pass
            elif a_count_l > b_count_l:
                times_remove = a_count_l - b_count_l
                a = a.replace(l,"", times_remove)
                counter += times_remove
            else:
                times_remove = b_count_l - a_count_l
                b = b.replace(l, "", times_remove)
                counter += times_remove
        else:
            counter += a.count(l)
            counter += b.count(l)
            a = a.replace(l, "")
            b = b.replace(l, "")

print(counter)
