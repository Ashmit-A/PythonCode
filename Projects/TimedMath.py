import time
import random

start_time = time.time()
score = 0

for _ in range(5):
    a, b = random.randint(1, 10), random.randint(1, 10)
    op = random.choice(['+', '-', '*'])
    if op == '+':
        correct_answer = a + b
    elif op == '-':
        correct_answer = a - b
    else:
        correct_answer = a * b
    
    answer = input(f"What is {a} {op} {b}? ")
    if answer.isdigit() and int(answer) == correct_answer:
        score += 1

end_time = time.time()

print(f"Your score: {score}/5. Time taken: {end_time - start_time:.2f} seconds.")
