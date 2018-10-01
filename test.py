data = ["HETATM", "1", "C", "-10.795197", "7.536659", "-9.040901"]

for y in range(3, 6):
    if float(data[y]) < 10 and "-" not in data[y] and len(data[2]) == 1:  # numbers 1-9 (without '-') and element = 1 char
        data[y] = data[y].rjust(len(data[y])+19)
        print(data[y])
    elif float(data[y]) > 10 and "-" not in data[y] and len(data[2]) == 1:  # numbers 1-infinity (without '-') and element = 1 char
        data[y] = data[y].rjust(len(data[y])+18)
        print(data[y])
    elif float(data[y]) > -10 and "-" in data[y] and len(data[2]) == 1:  # numbers 1-9 (with '-') and element = 1 char
        data[y] = data[y].rjust(len(data[y])+18)
        print(data[y])
    elif float(data[y]) < -10 and "-" in data[y] and len(data[2]) == 1:  # numbers 10-infinity (with '-') and element = 1 char
        data[y] = data[y].rjust(len(data[y]) + 17)
        print(data[y])


for y in range(3, 4):
    if float(data[y]) < 10 and "-" not in data[y] and len(data[2]) == 2:  # numbers 1-9 (without '-') and element = 2 char
        data[y] = data[y].rjust(len(data[y])+18)
        print(data[y])
    elif float(data[y]) > 10 and "-" not in data[y] and len(data[2]) == 2:  # numbers 1-infinity (without '-') and element = 2 char
        data[y] = data[y].rjust(len(data[y])+17)
        print(data[y])
    elif float(data[y]) > -10 and "-" in data[y] and len(data[2]) == 2:  # numbers 1-9 (with '-') and element = 2 char
        data[y] = data[y].rjust(len(data[y])+17)
        print(data[y])
    elif float(data[y]) < -10 and "-" in data[y] and len(data[2]) == 2:  # numbers 10-infinity (with '-') and element = 2 char
        data[y] = data[y].rjust(len(data[y]) + 16)
        print(data[y])




