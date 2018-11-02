import decimal
import glob
import os


OutFileNames = []
OutData = []

RunFileNames = []
RunData = []

skipFileOut = False
SkipFileRun = False
path = "C:/Users/Luke/PycharmProjects/ChemistryScripts/ohmstedelv/ohmstedelv"


OutFileNames.append("C:/Users/Luke/PycharmProjects/ChemistryScripts/ohmstedelv/cob-his3-hmovedB1.run")

# reading .out files and parsing out "Final Geometry Coordinates" 'XYZ' and element symbol
for y in range(len(OutFileNames)):
    with open(RunFileNames[y], "r") as openFile:
        Run_file_name = RunFileNames[y]
        for line in openFile:
            if "CONSTRAINTS" in line:
                SkipFileRun = True  # If "Constraints" in file, allows for it to enter "formator" function
                while "Block" not in line:
                    line = openFile.__next__()
                    if "Block" in line:
                        break
                    else:
                        RunData.append(line)

        if skipFile is True:
            for x in range(len(RunData)):
                initial_list = ','.join(RunData[x].split())
                build = [x.strip() for x in initial_list.split(',')]

                if "DIST" in build[0]:
                    build[0] = 'BOND RESTRAINT'
                    build.extend(("2.0000", "0.0000000"))
                elif "DIHED" in build[0]:
                    build[0] = 'TORSION RESTRAINT'
                    build.extend(("1.00000", "0.0000"))
                elif "ANGLE" in build[0]:
                    build[0] = 'ANGLE RESTRAINT'
                    build.extend(("1.00000", "0.0000"))

                for i in range(len(build)):
                    if "." not in build[i] and "RESTRAINT" not in build[i]:
                        build[i] = build[i].ljust(len(build[i]) + 3)
                    elif "RESTRAINT" in build[i]:
                        build[i] = build[i].ljust(len(build[i]) + 3)
                    elif "." in build[i] and "RESTRAINT" not in build[i]:
                        if i == len(build):
                            build[i] = build[i].ljust(len(build[i]) + 2)
                        else:
                            build[i] = build[i].ljust(len(build[i]) + 1)

                formatted_line = "".join(build)
                print(formatted_line)


