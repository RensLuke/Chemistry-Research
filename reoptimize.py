"""
    File name: reoptimize.py
    Author: Luke Rens
    Date created: 11/6/2018
    Description: Creates optimized .run child by adding constraints to its parent
    Python Version: 3.6.3
"""

import os

optimizedData = []


# TODO add header block with a description of what insertconstraints does

def insertconstraints(ATOM_INDEX):

    # TODO comment code

    newoptimizeddata = []

    number_of_constraints = input("How many Constraints would you like to add? ")

    counter = 0
    while counter != int(number_of_constraints):
        selection = input("What kind of constraints? [1] DIHED [2] DIST [3] ANGLE ")
        if int(selection) == 1:  # DIHED
            print("Enter constrain information: ")
            DIHED = "1 3 1.53"
            newoptimizeddata.append("DIHED " + DIHED)
            counter = counter + 1
        elif int(selection) == 2:  # DIST
            print("Enter constrain information: ")
            DIST = "1 3 1.53"
            newoptimizeddata.append("DIST " + DIST)
            counter = counter + 1
        elif int(selection) == 3:  # ANGLE
            print("Enter constrain information: ")
            ANGLE = "1 3 1.53"
            newoptimizeddata.append("ANGLE " + ANGLE)
            counter = counter + 1

    newoptimizeddata.insert(0,"CONSTRAINTS")
    newoptimizeddata.append("END")

    for i in range(len(newoptimizeddata)):
        if i == 0:
            optimizedData.insert(ATOM_INDEX - 2, newoptimizeddata[len(newoptimizeddata) - 1 - i])
        else:
            optimizedData.insert(ATOM_INDEX - 2, newoptimizeddata[len(newoptimizeddata) - 1 - i] + '\n')


# optimizedData = input("Please select file you would like to optimize ")

# TODO directory selection, same as ADFtoReaxFF

optimizedChild = "C:/Users/Luke/PycharmProjects/ChemistryScripts/ohmstedelv\water.run"

if os.path.exists(optimizedChild):
    with open(optimizedChild, "r") as openFile:
        for line in openFile:
            optimizedData.append(line)

# TODO function to exchange for new XYZ coordinates in Atoms block

for x in range(len(optimizedData)):
    if "Atoms" in optimizedData[x]:
        insertconstraints(x)
        break

for x in range(len(optimizedData)):
    print(optimizedData[x], end=" ")



