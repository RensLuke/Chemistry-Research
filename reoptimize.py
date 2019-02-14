"""
    File name: reoptimize.py
    Author: Luke Rens
    Date created: 11/6/2018
    Description: Creates optimized .run child by adding constraints to its parent
    Python Version: 3.6.3
"""

import os

# Global Variables
optimizedData = []


# TODO add header block with a description of what insertconstraints does

def insertconstraints(ATOM_INDEX):

    # TODO comment code

    newoptimizeddata = []

    number_of_constraints = input("How many Constraints would you like to add? ")

    counter = 0
    while counter != int(number_of_constraints):
        selection = input("What kind of constraint? [1] DIHED [2] DIST [3] ANGLE ")
        # DIHED
        if int(selection) == 1:
            interselection = input("Enter constrain information or press [q] to go back to selection menu: ")
            if interselection == 'q':
                continue
            else:
                newoptimizeddata.append("DIHED " + interselection)
                counter = counter + 1

        # DIST
        elif int(selection) == 2:
            interselection = input("Enter constrain information or press [q] to go back to selection menu: ")
            if interselection == 'q':
                continue
            else:
                newoptimizeddata.append("DIST " + interselection)
                counter = counter + 1

        # ANGLE
        elif int(selection) == 3:
            interselection = input("Enter constrain information or press [q] to go back to selection menu: ")
            if interselection == 'q':
                continue
            else:
                newoptimizeddata.append("ANGLE " + interselection)
                counter = counter + 1

    # conditional statement so file is only manipulated if user enters a constraint
    if int(number_of_constraints) > 0:
        newoptimizeddata.insert(0, "CONSTRAINTS")
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



