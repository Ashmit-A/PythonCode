def palindrome(input):
    a=str(input)
    if a == a[::-1]:
        return True
    return False

a = input("Enter number here: ")
print(palindrome(a))

def palindrome2(s):
    if len(s)<1:return "Palindrome"
    if s[0]==s[-1]: return palindrome2(s[1:-1])
    return "Not a plaindrome"

a = "racecar"
print(palindrome2(a))