""" 
    File name: ADFtoReaxFF.py
    Author: Luke Rens
    Date created: 9/17/2018
    Description: Creates a geo file from an optimized output file (.out) and constraints from its corresponding (.run) file
    Python Version: 3.6.3
"""

import glob
import decimal
import os

# TODO add description for addconstraints method and comments


def addconstraints(out_filename):
    run_data = []
    build = []

    run__file__path = out_filename[:-4] + ".run"

    if os.path.exists(run__file__path):
        with open(run__file__path, "r") as openFile:
            for file_line in openFile:
                if "CONSTRAINTS" in file_line:
                    while "END" not in file_line:
                        file_line = openFile.__next__()
                        if "END" in file_line:
                            break
                        elif "::" in file_line:
                            continue
                        else:
                            run_data.append(file_line)

        for x in range(len(run_data)):
            initial_list = ','.join(run_data[x].split())
            build = [x.strip() for x in initial_list.split(',')]

            if "DIST" in build[0]:
                build[0] = 'BOND RESTRAINT'
                build.extend(("7500.00","2.0000", "0.0000000"))
            elif "DIHED" in build[0]:
                build[0] = 'TORSION RESTRAINT'
                build.extend(("250.00","1.00000", "0.0000"))
            elif "ANGLE" in build[0]:
                build[0] = 'ANGLE RESTRAINT'
                build.extend(("1.00000", "0.0000"))

            # TODO add correct spacing to all constraints
            if 'BOND RESTRAINT' in build[0]:
                build[len(build)-1] = build[len(build)-1].rjust(len(build[len(build)-1]) + 2)
                build[len(build)-2] = build[len(build)-2].rjust(len(build[len(build)-2]) + 2)
                build[len(build)-3] = build[len(build)-3].rjust(len(build[len(build)-3]) + 1)
                build[len(build)-4] = decimalformat(build[len(build)-4])
                build[len(build) - 4] = build[len(build) - 4].rjust(len(build[len(build) - 4]) + 3)
                build[0] = build[0].ljust(len(build[0]) + 1)

                for i in range(len(build)-5, 0, -1):
                    build[i] = build[i].rjust(len(build[i]) + 2)

            elif 'TORSION RESTRAINT' in build[0]:
                build[len(build) - 1] = build[len(build) - 1].rjust(len(build[len(build) - 1]) + 2)
                build[len(build) - 2] = build[len(build) - 2].rjust(len(build[len(build) - 2]) + 2)
                build[len(build) - 3] = build[len(build) - 3].rjust(len(build[len(build) - 3]) + 1)
                build[len(build) - 4] = decimalformat(build[len(build) - 4])
                build[len(build) - 4] = build[len(build) - 4].rjust(len(build[len(build) - 4]) + 3)
                build[0] = build[0].ljust(len(build[0]) + 1)

                for i in range(len(build) - 5, 0, -1):
                    build[i] = build[i].rjust(len(build[i]) + 2)

            elif 'ANGLE RESTRAINT' in build[0]:
                build[len(build) - 1] = build[len(build) - 1].rjust(len(build[len(build) - 1]) + 2)
                build[len(build) - 2] = build[len(build) - 2].rjust(len(build[len(build) - 2]) + 2)
                build[len(build) - 3] = build[len(build) - 3].rjust(len(build[len(build) - 3]) + 1)
                build[len(build) - 4] = decimalformat(build[len(build) - 4])
                build[len(build) - 4] = build[len(build) - 4].rjust(len(build[len(build) - 4]) + 3)
                build[0] = build[0].ljust(len(build[0]) + 1)

                for i in range(len(build) - 5, 0, -1):
                    build[i] = build[i].rjust(len(build[i]) + 2)

            formatted_line = "".join(build)
            print(formatted_line)
    run_data.clear()
    build.clear()


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

# TODO if you have over 100 elements in index 2 spacing messes up as it is only deigned to hold 99 elements


def formator(out_file_data, out_filename):
    out_file_data.pop(0)

    # Assigning header to each file going into geo file
    print("BIOGRF 200")
    print("DESCRP " + out_filename[out_filename.find("\\")+1:-4])
    print("REMARK Created by RensScript")
    print("RUTYPE SINGLE POINT")
    # if .out's corresponding .run file has constraints inside, add them
    addconstraints(out_filename)

    # for loop iterates through 'out_file_data" which each item is a X,Y,Z coordinate and its element
    for x in range(len(out_file_data)):
        initial_list = ','.join(out_file_data[x].split())

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

# Variables for .out files
All_OutFile_Names = []
XYZ_Coordinates = []
skip_if_no_Coords = False


# TODO ask Dr. Ivancic for help on a better way to deal with file directories

path = "C:/Users/Luke/PycharmProjects/ChemistryScripts/ohmstedelv"

# Storing names of all .out files from specified directory
for file in glob.glob(os.path.join(path, '*.out')):
    All_OutFile_Names.append(file)

# reading .out files and parsing out "Final Geometry Coordinates" 'XYZ' and element symbol
for y in range(len(All_OutFile_Names)):
    with open(All_OutFile_Names[y], "r") as openOut:
        OutFile_Names = All_OutFile_Names[y]
        for line in openOut:
            if "Calculating Energy Terms for Final Geometry" in line:
                skip_if_no_Coords = True  # If "Final Geometry Coordinates" in file, allows for it to enter "formator" function
                line = openOut.__next__()
                while "<" not in line:
                    line = openOut.__next__()
                    if "<" in line:
                        break
                    else:
                        XYZ_Coordinates.append(line)

        # If final coordinates are found, format them
        if skip_if_no_Coords is True:
            formator(XYZ_Coordinates, OutFile_Names)  # generate Fortran file(takes Final Geometry Coordinates & File Name )
            skip_if_no_Coords = False
            XYZ_Coordinates.clear()  # clears list from previous file

