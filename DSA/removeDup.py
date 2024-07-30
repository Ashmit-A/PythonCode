dict = {}
a = [1,2,3,4,5,5,5,5,5]

for i in range(len(a)):
    dict[a[i]]="placeholder"

for i in dict:
    print(i)