'''sum of list'''

def add(list,n):
    if n==0 : return 0
    else: return list[n-1] + add(list,n-1)

list1 = [1,2,2,3,4,5,5,6,7,7,78,8,8,8]
print(add(list1, len(list1)))

'''palindrome'''

def palindrome(s):
    if len(s)<1:return "Palindrome"
    if s[0]==s[-1]: return palindrome(s[1:-1])
    return "Not a plaindrome"

a = "racecar"
print(palindrome(a))