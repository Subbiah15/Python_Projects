import random

def spin():
    emoji=['♣️','♦️','❤️','️♠️','🤑']
    result=[]
    for i in range(3):
        result.append(random.choice(emoji))
    return result

def print_spin(lucky_spin):
    print()
    print("\t|\t".join(lucky_spin))

def game_status(lucky_spin,bet_calculation):
    if lucky_spin[0] == lucky_spin[1] == lucky_spin[2]:
        print(f"\tYou WON! 💸 ${bet_calculation:.2f}\n")
    else:
        print("\tYou Lost!\n")

def verify_payment(lucky_spin , bet):
    if lucky_spin[0] == lucky_spin[1] == lucky_spin[2]:
        if lucky_spin[0]=='♣️':
            return 2*bet
        elif lucky_spin[0]=='♦️':
            return 3*bet
        elif lucky_spin[0]=='❤️':
            return 5*bet
        elif lucky_spin[0]=='♠️':
            return 10*bet
        elif lucky_spin[0]=='🤑':
            return 50*bet
    return 0
def main():
    purse=1000
    spinning='y'
    print("-------------------------------------")
    print("\tWelcome to the Lucky Spinner")
    print("-------------------------------------")
    print("\t\tEmoji : ♣️ ♦️ ❤️ ♠️ 🤑")
    print("\t\t\tBet Points\n\t\t\t♣️ : 2X \n\t\t\t♦️ : 3X \n\t\t\t❤️ : 5X \n\t\t\t♠️ : 10X \n\t\t\t🤑 : 50X")
    print("-------------------------------------")
    while spinning!='0':
        print("*************************************")
        print(f"You Current Purse Amount💸 : ${purse:.2f}")
        print("*************************************")
        bet=int(input("Enter your Bet Amount : "))
        print("*************************************")
        if bet > purse:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("\t  Insufficient Bet Amount")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            spinning='y'
        elif bet <= 0:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("  Bet Amount must be greater than 0")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            spinning='y'
        else:
            lucky_spin = spin()
            print_spin(lucky_spin)
            bet_calculation=verify_payment(lucky_spin , bet)
            game_status(lucky_spin,bet_calculation)

            if bet_calculation==0:
                purse=purse-bet
            else:
                purse=purse+bet_calculation

            if purse==0:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("\t\tYour Purse is Empty.")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                break

            spinning=input("Press any key to Spin Again...\n0 to quit")

    print("\n**************************************")
    print(f"  Your Final Purse Amount 💸: ${purse:.2f}")
    print("\t\tThanks For Playing")
    print("**************************************")

if __name__ == "__main__":
    main()