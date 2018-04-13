# Heya! This is an experiment by Chris Natcharian.
# A very simple programming language of this form:
# Pa (print var a) Sa3 (set a to 3) Cab (copy a to b)

# This file is a command line Letterbox interpreter.

import letterbox as l

lb = l.Letterbox() # Instantiate our core

print(": LETTERBOX :\n"
      + ": An experimental language \n"
      + ": (c) 2018 Chris Natcharian \n")

while(True):
    line = input("=> ")
    if line == "Q":
        break
    if line == "H":
        with open("README.txt", "r") as doc:
            print(doc.read())
            continue
    if line[0] == "F":
        try:
            with open(line[2:], "r") as file:
                for fline in file.readlines():
                    if fline[-1] == '\n':
                        fline = fline[:-1] # removes \n from end of line
                    if len(fline) == 0: continue
                    lb.set_input(fline)
                    lb.parse_exec()
                    out = lb.get_output()
                    if out != "":
                        print(out)
                    if "ERROR" in out:
                        break
                    lb.clear_output()
        except FileNotFoundError:
            print("ERROR in F: File not found.")
        break

    lb.set_input(line)
    lb.parse_exec()
    out = lb.get_output()
    if out != "":
        print(out)
    lb.clear_output()

print("\n")