def lengthOfLast(s):
    length = 0
    i = len(s) - 1

    while i >= 0 and s[i] == ' ':
        i -= 1

    while i >= 0 and s[i] != ' ':
        length += 1
        i -= 1

    return length

str = "fjgr lgrejgl hello"
result = lengthOfLast(str)
print("Length of the last word:", result)