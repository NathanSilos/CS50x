from cs50 import get_float

# Declaring variables
change = get_float("Change owed: ")
coins = 0

# Checking if change is right 
while change <= 0.00:
    change = get_float("Change owed: ")
    
# round change
change = round(change * 100)

# starting counting coins
while change > 0:
    # Subtract 25 of change
    while change >= 25:
        change -= 25
        coins += 1
    # Subtract 10 of change    
    while change >= 10:
        change -= 10
        coins += 1
    # Subtract 5 of change    
    while change >= 5:
        change -= 5
        coins += 1
    # Subtract 1 of change    
    while change >= 1:
        change -= 1
        coins += 1
# Print how many coins you're gonna need it
print(coins)