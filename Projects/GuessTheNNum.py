import random

print("===================================")
print("=   Welcome to Guess The Number   =")
print("===================================")

answer = random.randrange(1,100)
guess = 0

while True:
    guess = input("\nEnter Your Guess:")
    guess = int(guess)
    if(guess>answer):
        print("\nYour guess is higher than the number!")
    elif(guess<answer):
        print("\nYour guess is lower than the number!")
    elif(guess==answer):
        break

print("\nCorrect!!!")
print("\n======Thanks for playing :)=======")