def plusOne(digits):
        n = 0
        for element in digits:
            n = (n*10) + element
        print(n)
        
        n+=1

        new_digits = []
        while n > 0:
            new_digits.insert(0, n % 10)  
            n //= 10
        
        return new_digits

digits=[1,2,2]
print(plusOne(digits))