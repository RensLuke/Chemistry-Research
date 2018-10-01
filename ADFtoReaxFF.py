# Luke Rens ADF to ReaxFF script
import glob
import decimal

# creating a list of all .out files
allFiles = []
data = []
skip = False

# function format decimals


def decimalformat(num):
    d = decimal.Decimal(num)
    d = format(d, '.6f')
    return d


# function to create a fortran file


def formator(newData,fileName):
    newData.pop(0)
    print("BIOGRF 200")
    print("DESCRP " + fileName[:-4])
    print("REMARK Created by RensScript")
    print("RUTYPE SINGLE POINT")

    for x in range(len(newData)):
        strHold = ','.join(newData[x].split())

        # Conditional Statement to remove '.' from number (ex. 1. = 1, 12. = 12)
        if x < 9:
            strHold = strHold[2:]
        else:
            strHold = strHold[3:]

        # using ',' as a deliminator and storing into a list
        build = [x.strip() for x in strHold.split(',')]

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
        strHold2 = "".join(build)

        print(strHold2)

    print("END" + '\n')


# reading in file name using glob library,
# storing them in temp variable 'fileName'
# and storing them in list 'allFiles'
for file in glob.glob("*.out"):
    allFiles.append(file)

# printing out all file names(when needed)
# for x in range(len(allFiles)):
#    print(allFiles[x])

# opening each .out file stored in 'allFiles' list
# parsing line by line to find each 'Coordinates in Geometry Cycle' header
# once found, recording each 'Atom' and its corresponding 'XYZ' coordinates in 'data' list
for y in range(len(allFiles)):
    with open(allFiles[y], "r") as openFile:
        fileName = allFiles[y]
        for line in openFile:
            if "Calculating Energy Terms for Final Geometry" in line:
                skip = True  # If "Final Geometry Coordinates" is in file, allows for it to enter "formator" function
                line = openFile.__next__()
                while "<" not in line:
                    line = openFile.__next__()
                    if "<" in line:
                        break
                    else:
                        data.append(line)

        if skip is True:
            formator(data, fileName)  # method to generate Fortran file(takes Final Geometry Coordinates & File Name )
            skip = False
            data.clear()  # clears list from previous file

