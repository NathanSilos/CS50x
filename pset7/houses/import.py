from csv import reader, DictReader
from sys import argv, exit
from cs50 import SQL

# Creating a SQL variable to interate with data base
# to use >> db.execute("SQL QUERY")
db = SQL("sqlite:///students.db")

# Check if is the right file
if len(argv) != 2:
    print("Missing a .csv file!")
    exit(1)

name = str(argv[1])
tamanho = len(name)
if name[tamanho-4:tamanho] != ".csv":
    print("Wrong file")
    exit(1)

# Openning csv file
with open(argv[1], "r") as file:
    # Read the file
    reader = DictReader(file)
    for student in reader:
        # Declaring variables that Im gonna use
        name = student["name"]
        name = name.split()
        # Including names in data base
        if len(name) == 2:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, NULL, ?, ?, ?)",
                       name[0], name[1], student["house"], student["birth"])
        elif len(name) == 3:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)",
                       name[0], name[1], name[2], student["house"], student["birth"])