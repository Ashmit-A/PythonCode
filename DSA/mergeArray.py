def merge(num1, m, num2, n):
    i = m-1
    j = n-1
    k = m+n-1

    while(j>=0):
        if(i>=0 and num1[i]>num2[j]):
            num1[k]=num1[i]
            i-=1
        else:
            num1[k]=num2[j]
            j-=1
        k-=1