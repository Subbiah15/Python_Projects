from random import shuffle
import string

Char = " " + string.punctuation + string.digits + string.ascii_letters
Char = list(Char)
XChar = Char.copy()
shuffle(XChar)
#print(Char)
#print(XChar)

#ENCRYPTION
print("***************************************")
EM = input("Enter a Message to Encrypt : \t")
DM = ""

for letter in EM:
    i = Char.index(letter)
    DM = DM + XChar[i]

print(f"The Encrypted Message is   : \t{DM}")
print("***************************************")
print("---------------------------------------")
print(f"\t\t{EM}\t==>\t{DM}")
print("---------------------------------------")

#DECRYPTION
print("***************************************")
DM = input("Enter a Message to Decrypt : \t")
EM = ""

for letter in DM:
    i = XChar.index(letter)
    EM = EM + Char[i]

print(f"The Original Message is   : \t{EM}")
print("***************************************")
print("---------------------------------------")
print(f"\t\t{DM}\t==>\t{EM}")
print("---------------------------------------")