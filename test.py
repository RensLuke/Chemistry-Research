import glob
import os

All_OutFile_Names = []
RunData = []

IsConstraint = True
path = "C:/Users/Luke/PycharmProjects/ChemistryScripts/hold"

for file in glob.glob(os.path.join(path, '*.out')):
    All_OutFile_Names.append(file)


Run_File_Path = All_OutFile_Names[0][:-4] + ".run"

if os.path.exists(Run_File_Path):
    with open(Run_File_Path, "r") as openFile:
        for line in openFile:
            if "CONSTRAINTS" in line:
                SkipFileRun = True  # If "Constraints" in file, allows for it to enter "formator" function
                while "END" not in line:
                    line = openFile.__next__()
                    if "END" in line:
                        break
                    elif "::" in line:
                        continue
                    else:
                        RunData.append(line)

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
        # print(formatted_line)


print("DESCRP " + Run_File_Path[Run_File_Path.find("\\")+1:-4])

