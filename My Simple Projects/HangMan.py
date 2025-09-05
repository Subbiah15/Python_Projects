import random

words=("luffy","zoro","sanji","usopp","nami","chopper","franky","robin","brook","jimbei")
print(f"Pirate Ship Crew Members")
print(words)
hangman={0: ("\t  😀  ",
             "\t     ",
             "\t     "),
         1: ("\t  😐  ",
             "\t     ",
             "\t     "),
         2: ("\t  😐  ",
             "\t  ❗  ",
             "\t     "),
         3: ("\t  😐   ",
             "\t /❗   ",
             "\t     "),
         4: ("\t  😐   ",
             "\t /❗\\ ",
             "\t     "),
         5: ("\t  😐   ",
             "\t /❗\\ ",
             "\t  /   "),
         6: ("\t  😵   ",
             "\t /❗\\ ",
             "\t  /\\ "),
         }

def display_hangman(wrong_guesses):
    print("______________")
    for line in hangman[wrong_guesses]:
        print(line)
    print("______________\n")

def display_hint(hint):
    print("\t".join(hint))

def display_answer(answer):
    print("\t".join(answer))

def main():
    answer = random.choice(words)
    hint = ["_"]*len(answer)
    wrong_guesses = 0
    guessed_words = []
    display_hangman(wrong_guesses)
    display_hint(hint)
    playing = True
    Finished = False

    while playing:



        guess = input("Guess a letter: ").lower()


        if len(guess) != 1 or not guess.isalpha():
            print("Invalid Input. Please try again...")
            continue

        if guess in guessed_words:
            print("You Already Guessed this Letter...")
            continue

        guessed_words.append(guess)

        if guess in answer:
            for i in range(len(answer)):
                if answer[i] == guess:
                    hint[i] = guess
        else:
            wrong_guesses += 1



        if wrong_guesses >= 6:
            display_hangman(wrong_guesses)
            print("  Correct Answer")
            display_answer(answer)
            print("\n\tYou LOSE!")
            print("\tMan Hanged..")
            playing = False

        elif "_" not in hint:
            display_hangman(wrong_guesses)
            print("  Correct Answer")
            display_answer(answer)
            print("\n\t\tYou WIN!")
            print("\tYou Saved the Man..")
            finished = True
            playing = False

        else:
            display_hangman(wrong_guesses)
            display_hint(hint)

if __name__ == "__main__":
    main()