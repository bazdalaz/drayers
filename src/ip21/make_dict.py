import os
listfilesFILE= open("listfiles.txt")
xx_files=listfilesFILE.read().split("\n")

for path in xx_files:
    file = open(path)
    line = file.readline()
    outfile = open(os.path.splitext(path)[0][-1] + ".txt", "w", encoding="utf-8")
    outfile.writelines(file.readline())
    Filterlins = ("HPMM", "HLAI", "DI", "HLAI", "AO", "APMM", "DO", "AO_16")
    while line:
        line = file.readline()
        if any([FilterL in line for FilterL in Filterlins]):
            words_of_line = line.split("  ")
            words_of_line = [word for word in words_of_line if
                             not (word in ("", '!!', ' !!!', '!!!', '@@@', ' @@@'))]  # filter all spaces
            outfile.writelines(f"{words_of_line[0][1:]}\t {words_of_line[2]}\n")
    outfile.close()
    file.close()
