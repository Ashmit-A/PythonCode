def searchInsert(num, target):
        startMarker = 0
        endMarker = len(num) - 1
        while startMarker <= endMarker:
            mid = (startMarker + endMarker) // 2
            if num[mid] < target:
                startMarker = mid + 1
            elif num[mid] > target:
                endMarker = mid - 1
            else:
                return mid
        return startMarker

num = [1,4,6,2,9,8,1]
target=4
print(searchInsert(num,target))
