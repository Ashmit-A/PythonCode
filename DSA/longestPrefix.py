def longest_common_prefix(strings):
    if not strings:
        return ""

    strings.sort()
    
    prefix = strings[0]

    for string in strings:
        while not string.startswith(prefix):
            prefix = prefix[:-1]

    return prefix