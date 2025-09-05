questions=("1. Which is frontend programming language?",
           "2. Which is backend programming language?",
           "3. What sweet does subbu likes?",
           "4. what sports does subbu plays?",
           "5. How much price of 5rs Pen?",)
options=( ("A. Python", "B. C", "C. HTML/CSS", "D. Java"),
         ("A. Python","B. HTML/CSS","C. JavaScript","D. React.js"),
         ("A. Mysurpak", "B. Palkova", "C. Gulab Jamun", "D. Laddu"),
         ("A. Tennis", "B. VolleyBall","C. Cricket", "D. BasketBall"),
         ("A. 10","B. 15","C. 2","D. 5"))
answers=("C","A","B","C","D")
guesses=[]
score=0
q_num=0
for question in questions:
    print("------------------------------------------")
    print(question)
    for option in options[q_num]:
        print(option)
    guess=input("Enter the Correct Option(A,B,C,D): ").upper()
    while not (guess=="A" or guess=="B" or guess=="C" or guess=="D"):
        print("Invalid option")
        guess=input("Enter the Correct Option(A,B,C,D): ").upper()
    guesses.append(guess)
    if guess==answers[q_num]:
        score+=1
        print("Correct!")
    else:
        print("Wrong!")
        print("The Correct Answer:",answers[q_num])

    q_num+=1
print("------------------------------------------")
print(f"Correct Answers: {answers}")
print(f"Your Guesses: {guesses}")
print("Total Score:",(score/q_num)*100,"%")
print("------------------------------------------")