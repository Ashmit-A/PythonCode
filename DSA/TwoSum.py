def TwoSum(arr, target):
    n=len(arr)

    def findPos(index, remainder):
        if index == n:
            return False
        if arr[index]==remainder:
            return index
        else:
            return findPos(index + 1, remainder)

    for i in range(n):
        remainder= target-arr[i]
        if findPos(i+1,remainder):
            return i,findPos(i+1,remainder)

array = [1,3,4,5,7]
target = 7
print(TwoSum(array,target))