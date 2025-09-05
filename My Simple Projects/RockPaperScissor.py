import random
options = ('rock', 'paper', 'scissor')
computer=random.choice(options)
PlayAgain = "y"
Score=0
Matches=0
while(PlayAgain=="y"):
    player = input("1. rock\n2. paper\n3. scissor\nEnter your option : ")
    if player == computer:
        print("Computer :", computer)
        print("Player :", player)
        print("Tie")
        Matches+=1
    elif (player == "rock" and computer == "paper") or (player == "paper" and computer == "scissor") or (player == "scissor" and computer == "rock"):
        print("Computer :", computer)
        print("Player :", player)
        print("You Lose")
        Matches+=1
    elif (player == "rock" and computer == "scissor") or (player == "scissor" and computer == "paper") or (player == "paper" and computer == "rock"):
        print("Computer :", computer)
        print("Player :", player)
        print("You Win")
        Score+=1
        Matches+=1
    else:
        print("Invalid option. Try again")
        PlayAgain = "yes"

    PlayAgain = input("Do you want to play again? (y/n): ").lower()
print("\n-----------------------------")
print(f"\tYour Score is: {Score} / {Matches}")
print("-----------------------------\n")
print("Thanks you for Playing!")
