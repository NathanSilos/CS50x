from csv import reader, DictReader
from sys import argv, exit
from cs50 import SQL

# Creating a SQL variable to interate with data base
# to use >> db.execute("SQL QUERY")
db = SQL("sqlite:///students.db")

# Check if the input is right
if len(argv) != 2:
    print("Missing the house")
    exit(1)

# execute a fucking query
house = db.execute("SELECT first, middle, last, birth FROM students WHERE house LIKE ? ORDER BY last, first", argv[1])

# print output
for student in house:
    if (not isinstance(student["middle"], str)):
        print(f"{student['first']} {student['last']}, born {student['birth']}")
    else:
        print(f"{student['first']} {student['middle']} {student['last']}, born {student['birth']}")