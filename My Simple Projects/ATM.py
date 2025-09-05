def balance(bal):
    print("***************************************")
    print(f"\tYour Current Balance : ${bal:.2f}")
    print("***************************************")

def deposit():
    print("***************************************")
    amount=float(input("\tEnter your Deposit Amount : "))
    print("***************************************")
    if amount <= 0:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Invalid Deposit Amount. Amount must be greater than 0")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return 0
    else:
        return amount

def withdraw(bal):
    print("***************************************")
    amount=float(input("\tEnter your Withdraw Amount : "))
    print("***************************************")
    if amount <= 0:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Invalid Withdraw Amount. Amount must be greater than 0")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return 0
    elif amount > bal:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("\tInsufficient Balance")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return 0
    else:
        return amount

def main():
    bal=0
    again='y'
    while again!='n':
        print("***************************************")
        print("\t\tWelcome to ATM Service")
        print("***************************************")
        print("\t\t1. Check Balance\n\t\t2. Deposit\n\t\t3. Withdraw\n\t\t4. Exit")
        print("***************************************")
        choice=int(input("Enter your Transaction Method(1-4) : "))
        match choice:
            case 1:
                balance(bal)
                again=input("Do you want to continue transaction? (y/n) : ").lower()
                print("***************************************")
            case 2:
                bal += deposit()
                balance(bal)
                again=input("Do you want to continue transaction? (y/n) : ").lower()
                print("***************************************")
            case 3:
                bal -= withdraw(bal)
                balance(bal)
                again=input("Do you want to continue transaction? (y/n) : ").lower()
                print("***************************************")
            case 4:
                again='n'
            case _:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("Invalid Transaction Method. Select from 1-4")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                again = 'y'

    print("\n#####_/\_Thank you for your transaction_/\_#####\n")

if __name__=="__main__":
    main()
