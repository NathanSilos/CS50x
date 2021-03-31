from cs50 import get_int

# Declaring variables
space = ' '
hsh = '#'
n = 1

# Getting height
height = get_int("Height: ")

# Check if height is right
while height <= 0 or height >= 9:
    height = get_int("Height: ")

# constructing the pyramid
for i in range(height):
    print(space * (height - (i + 1)), end='')
    print(hsh * (i + 1), end='')
    print()