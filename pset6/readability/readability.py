# Declaring variables
text = input("Text: ")
letters = 0
# Counting sentences
sentences = text.count(".") + text.count('!') + text.count('?')

# Counting words 
words = len(text.split())stu

# Counting letters
letters = len(text) - (sentences + text.count(' ') + text.count('"') + text.count(",") +
                       text.count(":") + text.count("'") + text.count(";") + text.count("-"))

# Calculating values
L = letters / words * 100
S = sentences / words * 100

# Calculating Grade
grade = round(0.0588 * L - 0.296 * S - 15.8)

# Showing each grade
if grade < 1:
    print("Before Grade 1")
elif grade <= 16:
    print("Grade", grade)
else:
    print("Grade 16+")