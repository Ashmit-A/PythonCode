def roman_to_decimal(roman):
    roman_numerals = {'I': 1,
                      'V': 5, 
                      'X': 10,
                      'L': 50, 
                      'C': 100, 
                      'D': 500, 
                      'M': 1000}
    answer = 0
    pre_value = 0
    
    for numeral in reversed(roman):
        value = roman_numerals[numeral]
        
        if value < pre_value:
            answer -= value
        else:
            answer += value
        pre_value = value
    return answer


a = input("Enter a Roman numeral: ")
print(f"The answer equivalent is: {roman_to_decimal(a.upper())}")