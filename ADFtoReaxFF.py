# Luke Rens ADF to ReaxFF script
import glob
import decimal


""" Decimal Format function:
Decimal Format is used to take all 'X', 'Y' and 'Z' numbers and put them all to a unified decimal format. Can be 
modified to support any decimal format.
"""


def decimalformat(num):
    d = decimal.Decimal(num)
    d = format(d, '.6f')
    return d


""" Formator function:
Formator takes in a list of string and the file name the list of strings came from. Each string consists of
10 items which are separated into a new list where each index represents a item. Correct spacing is added
to each item in the list(going from index 9 to 0) and then joined back together into a string. These string are
the written to "geo" to create "geo.f". Each time Formator is ran, a new geo file is created to be ran through ReaxFF. 
"""


def formator(new_data, name):
    new_data.pop(0)
    print("BIOGRF 200")
    print("DESCRP " + name[:-4])
    print("REMARK Created by RensScript")
    print("RUTYPE SINGLE POINT")

    for x in range(len(new_data)):
        initial_list = ','.join(new_data[x].split())

        # Conditional Statement to remove '.' from number (ex. 1. = 1, 12. = 12)
        if x < 9:
            initial_list = initial_list[2:]
        else:
            initial_list = initial_list[3:]

        # using ',' as a deliminator and storing into a list
        build = [x.strip() for x in initial_list.split(',')]

        # Conditional Statement to shift spaces of numbers < 9 over one space
        if x < 9:
            build.insert(0, "HETATM")
        else:
            build.insert(0, "HETATM")

        # Inserting list number and 1 & 0 in the back of the string
        build.insert(1, str(x + 1))
        build.insert(6,build[2])
        build.insert(7, '1')
        build.insert(8, '1')

        build.insert(9, '0.0')

        build[9] = build[9].rjust(len(build[9]) + 2)  # Spacing for 0.0
        build[8] = build[8].rjust(len(build[8]) + 1)   # Spacing for 1

        # Spacing for last 1 & conditional testing for if its a 1 or 2 letter element
        if len(build[6]) == 2:
            build[7] = build[7].rjust(len(build[7]) + 2)
        else:
            build[7] = build[7].rjust(len(build[7]) + 3)

        build[6] = build[6].rjust(len(build[6]) + 3)  # Spacing for last element

        # formatting all "X,Y,Z" to 6 decimal places
        for y in range(3, 6):
            build[y] = decimalformat(build[y])

        # adjust spacing for "Y,Z"
        for y in range(4, 6):
            if float(build[y]) < 10 and "-" not in build[y]:
                build[y] = build[y].rjust(len(build[y]) + 3)
            elif float(build[y]) > 10 and "-" not in build[y]:
                build[y] = build[y].rjust(len(build[y]) + 2)
            elif float(build[y]) > -10 and "-" in build[y]:
                build[y] = build[y].rjust(len(build[y]) + 2)
            elif float(build[y]) < -10 and "-" in build[y]:
                build[y] = build[y].rjust(len(build[y]) + 1)

        # adjust spacing for "X"
        if float(build[3]) < 10 and "-" not in build[3] and len(
                build[2]) == 1:  # numbers 1-9 (without '-') and element = 1 char
            build[3] = build[3].rjust(len(build[3]) + 19)
        elif float(build[3]) > 10 and "-" not in build[3] and len(
                build[2]) == 1:  # numbers 1-infinity (without '-') and element = 1 char
            build[3] = build[3].rjust(len(build[3]) + 18)
        elif float(build[3]) > -10 and "-" in build[3] and len(
                build[2]) == 1:  # numbers 1-9 (with '-') and element = 1 char
            build[3] = build[3].rjust(len(build[3]) + 18)
        elif float(build[3]) < -10 and "-" in build[3] and len(
                build[2]) == 1:  # numbers 10-infinity (with '-') and element = 1 char
            build[3] = build[3].rjust(len(build[3]) + 17)
        elif float(build[3]) < 10 and "-" not in build[3] and len(
                build[2]) == 2:  # numbers 1-9 (without '-') and element = 2 char
            build[3] = build[3].rjust(len(build[3]) + 18)
        elif float(build[3]) > 10 and "-" not in build[3] and len(
                build[2]) == 2:  # numbers 1-infinity (without '-') and element = 2 char
            build[3] = build[3].rjust(len(build[3]) + 17)
        elif float(build[3]) > -10 and "-" in build[3] and len(
                build[2]) == 2:  # numbers 1-9 (with '-') and element = 2 char
            build[3] = build[3].rjust(len(build[3]) + 17)
        elif float(build[3]) < -10 and "-" in build[3] and len(
                build[2]) == 2:  # numbers 10-infinity (with '-') and element = 2 char
            build[3] = build[3].rjust(len(build[3]) + 16)

        # Spacing for first element & conditional testing for if its a 1 or 2 letter element
        if len(build[2]) == 2:
            build[2] = " " + build[2]
        else:
            build[2] = " " + build[2]

        # Spacing for number & conditional testing for if its a > 9 or < 9
        if len(build[1]) == 2:
            build[1] = "    " + build[1]
        else:
            build[1] = "     " + build[1]

        # forming string from each line, then printing (or writing to a fortran file)
        formatted_line = "".join(build)

        print(formatted_line)

    print("END" + '\n')


"""Main routine:
Main routine stores in all .out files from a specified directory and stores them in list 'fileNames'.
Each .out is read one at a time, parsing line by line to find "Final Geometry Coordinates" and pulling
out its element symbol and 'XYZ' coordinates. Once all data is found from .out file, it is then passed
to formator to have correct spacing added so a 'geo' file can be created.
"""

fileNames = []
fileData = []
skipFile = False

# Storing names of all .out files from specified directory
for file in glob.glob("*.out"):
    fileNames.append(file)

# reading .out files and parsing out "Final Geometry Coordinates" 'XYZ' and element symbol
for y in range(len(fileNames)):
    with open(fileNames[y], "r") as openFile:
        file_name = fileNames[y]
        for line in openFile:
            if "Calculating Energy Terms for Final Geometry" in line:
                skipFile = True  # If "Final Geometry Coordinates" in file, allows for it to enter "formator" function
                line = openFile.__next__()
                while "<" not in line:
                    line = openFile.__next__()
                    if "<" in line:
                        break
                    else:
                        fileData.append(line)

        if skipFile is True:
            formator(fileData, file_name)  # generate Fortran file(takes Final Geometry Coordinates & File Name )
            skipFile = False
            fileData.clear()  # clears list from previous file

