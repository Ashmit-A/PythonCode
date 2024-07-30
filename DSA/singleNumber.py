def singleNum(numbers):
    single = set()
    for num in numbers:
        if(num in single):
            single.remove(num)
        else: single.add(num)
    
    return single

arr = [1]
print(singleNum(arr))