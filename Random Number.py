#Imports the random package so I can use random. functions
import random

#Defines my target
target = random.randint(1, 100)

#Print prompt
print("Pick a number between 1 and 100!")

guess = 0

#Runs until guess is correct
while guess != target:
    
    #Defines guess using prompt
    guess = input(("Your guess: "))

    #Checks if input is a number, asks until it is
    while guess.isdigit() != True:
        print("That's not a number!")
        guess = input(("Your guess: "))
        
    #Casts guess as int
    guess = int(guess)
        
    #Checks for if guess is higher or lower and tells user accordingly
    if guess < target:
        hilow = "higher"
        print(f"Your guess was {guess}, but the number is {hilow}.")
    elif guess > target:
        hilow = "lower"
        print(f"Your guess was {guess}, but the number is {hilow}.")

#Once they make the correct guess the loop will stop and print the answer
print(f"You're right! The number was {target}! Good job!")
    
   
    

