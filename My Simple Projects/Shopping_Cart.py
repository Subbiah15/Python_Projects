print("-------------------------------------")
print("*******!Welcome to Subbu Cafe!******")
print("-------------------------------------")
menu={ "Samosa":10,
       "Baji":8,
       "Tea":12,
       "Ginger tea":14,
       "Coffee":15,
       "Cold coffee":20,
       "Boost":15,
       "Butter biscuit":5,
       "Veg puffs":13,
       "Egg puffs":16,
       "Mushroom puffs":18,
       "Chicken puffs":20,
       "Veg roll":15,
       "Paneer roll":16,
       "Mushroom roll":18,
}
cart=[]
total=0
print("-----------MENU-----------")
for key,value in menu.items():
    print(f"{key:15}:Rs.{value:.2f}")
print("--------------------------")

while True:
    food=input("Enter your food(q to quit):").capitalize()
    if food.lower()=="q":
        break
    elif menu.get(food) is not None:
        cart.append(food)
    else:
        print("Please enter food which in in menu card")

print("-----------BILL-----------")
for food in cart:
    total += menu.get(food)
    print(f"{food:15} : Rs.{menu.get(food):.2f}",end="\n")
print("---------------------------")
print(f"Total\t\t\t: Rs.{total:.2f}")
print("---------------------------")
