# original code
def replace(s):
    changed = s
    for i in range(0, len(s)-1):
        if s[i] >='a' and s[i] <- 'z':
            changed[i] += s[i].upper()
        else:
            changed[i] += s[i]

    return changed

"""
line 4 is wrong. Range will always execute by default (0, len(s)-1). 
    So the current implementation now is (0, len(s)-1-1), this means we will miss the last character
lines 5 and 7 are wrong. 
    In Python, strings are immutable, so you can't change their characters in-place.
also the comparison in line 4 is not accurate.
    is preferred to use the build-in functionality str.isupper() or str.islower() 
iterate the string based on character length is not ideal since there is a more optimized way to do that
"""


# proposed changes are
def replace(s):
    changed = ""
    for i in range(0, len(s)):
        if s[i].islower():
            changed += s[i].upper()
        else:
            changed += s[i]

    return changed


# a more optimized version is
def replace(s):
    changed = ""
    for character in s:
        if character.islower():
            changed += character.upper()
        else:
            changed += character

    return changed