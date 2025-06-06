def isLongPressed(name, typed):
    n = len(name)
    m = len(typed)
    
    i,j= 0 

    while j < m:
        if i < n and name[i] == typed[j]:
            i+=1
            j+=1
        elif i<n and typed[j] == typed[j-1]:
            j+=1
        else:
            return False
    return i == len(name)
