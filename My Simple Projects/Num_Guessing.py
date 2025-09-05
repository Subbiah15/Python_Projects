import random
low=1
high=100
guess=random.randint(low,high)

while True:
    num = int(input("Enter a number (1 to 100): "))
    if num==guess:
        print("Your guess is correct!")
        break
    elif num>100 & num<1:
        print("Enter a number between 1 and 100")
    elif num>guess:
        print("Your guess is too high!")
    elif num<guess:
        print("Your guess is too low!")

print(guess)