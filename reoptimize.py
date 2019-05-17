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

def insertconstraints(ATOM_INDEX, doesConstraints):

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
    if doesConstraints and int(number_of_constraints) > 0:
        for i in range(len(newoptimizeddata)):
            if i == 0:
                optimizedData.insert(ATOM_INDEX - 1, newoptimizeddata[len(newoptimizeddata) - 1 - i] + '\n')
            else:
                optimizedData.insert(ATOM_INDEX - 1, newoptimizeddata[len(newoptimizeddata) - 1 - i] + '\n')
        optimizedData.insert(ATOM_INDEX+int(number_of_constraints)-1, "END\n")
    elif int(number_of_constraints) > 0:
        newoptimizeddata.insert(0, "CONSTRAINTS")
        for i in range(len(newoptimizeddata)):
            if i == 0:
                optimizedData.insert(ATOM_INDEX - 2, newoptimizeddata[len(newoptimizeddata) - 1 - i])
            else:
                optimizedData.insert(ATOM_INDEX - 2, newoptimizeddata[len(newoptimizeddata) - 1 - i] + '\n')
        optimizedData.insert(ATOM_INDEX+1, "\n END")


optimizedChild = " "
doesConstraints = False

while True:
    optimizedChild = input("Please enter input file path: ")
    # optimizedChild = "ohmstedelv/water.run"

    exists = os.path.exists(optimizedChild)
    if exists:
        print("Correct path")
        break
    else:
        print("Invalid file path")


with open(optimizedChild, "r") as openFile:
    for line in openFile:
        optimizedData.append(line)

# TODO function to exchange for new XYZ coordinates in Atoms block

for x in range(len(optimizedData)):
    if "CONSTRAINTS" in optimizedData[x]:
        doesConstraints = True
    if doesConstraints and "END" in optimizedData[x]:
        optimizedData.pop(x)
    if "Atoms" in optimizedData[x]:
        insertconstraints(x, doesConstraints)
        break

path_split = optimizedChild.split('/')
print("Old file name was: " + path_split[len(path_split) - 1])
newName = input("Enter New File Name (without .run): ")
newName = newName + ".run"
path_split[len(path_split) - 1] = newName
newPath = '/'.join(path_split)

with open(newPath, 'a+') as writer:
    for x in range(len(optimizedData)):
        writer.write(optimizedData[x])

print("Done")



