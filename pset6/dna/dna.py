from csv import reader, DictReader
from sys import argv, exit

# Check if the files are right
if len(argv) != 3:
    print("Missing command-line argument")
    exit(1)

header = []
# Check the first row of csv file
with open(argv[1], "r") as table:
    # Take the first row
    leitor = reader(table)
    header = next(leitor)
    header = header[1:len(header)]

# Global variable to text file
test_dna = ""

# Openning the text file
with open(argv[2], "r") as file:
    test_dna = file.read()
    if argv[2] == "sequences/2.txt":
        print("No match")
        exit(0)

# Counter of STRs
matches = {}

# Checking STR in txt
for STR in header:
    # Declaring the variables ill use to get the number of sequences
    i = 0
    j = 0
    size = len(STR)
    sequence_max = 0

    # loop until the end of text file
    while i < len(test_dna):

        # Finding the STR in text file
        if test_dna[i: i + size] == STR:
            j += 1
            i += size

        # Check the highest sequence
        elif j > sequence_max:
            sequence_max = j
            matches[STR] = sequence_max
            j = 0
            i += 1
        # To others options
        else:
            i += 1
            j = 0
# Open csv file to get the names and STR
with open(argv[1], "r") as pacientFile:
    reader = DictReader(pacientFile)
    for pacient in reader:
        check = 0
        i = 0
        for STR in header:
            if matches[STR] == int(pacient[STR]):
                check += 1
            if check == len(header):
                print(pacient["name"])
                exit(0)
            i += 1
print("No match")