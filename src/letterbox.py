# Heya! This is an experiment by Chris Natcharian.
# A very simple programming language of this form:
# Pa (print var a) Sa3 (set a to 3) Cab (copy a to b)

# This file is the core interpreter for the language.

class Letterbox:
    ### FIELDS ###

    input = ""  # An input string to read.
    output = ""  # Where all output gets put.
    data = {}  # Storage for variables.
    func = {} # Storage for function mappings.

    ### SETUP FUNCTIONS ###

    # Initializer
    def __init__(self):
        self.reset()
        self.set_func()

    # Reset function clears all stored data.
    def reset(self):
        self.reset_data()
        self.input = ""
        self.output = ""

    # Sets all vars to 0.
    def reset_data(self):
        self.data = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0,
                'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0,
                'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0,
                'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}

    # Creates a table of function mappings.  
    # Each function takes in a string as an argument.
    def set_func(self):
        self.func = {'P': self.print,
                     'S': self.store,
                     'C': self.copy,
                     'M': self.math,
                     'L': self.loop,
                     'I': self.ifs,
                     'R': self.res,
                     'G': self.getin,
                     'N': self.negate,
                     'B': self.bool}

    def set_input(self, instring):
        self.input = instring

    def setvar(self, char, val):
        self.data[char] = val

    def getvar(self, char):
        return self.data[char]

    def get_output(self):
        return self.output

    def clear_output(self):
        self.output = ""

    def isvar(self, char):
        return char in self.data

    def isfunc(self, char):
        return char in self.func

    def isnum(self, char):
        return char.isdigit()

    ### PROGRAM FUNCTIONS! ###
    # Each one takes a string of arguments.
    # Each returns one of two things:
    # - An error string.
    # - The number 0, meaning execution was successful.

    # Pa: Prints contents of a
    def print(self, args):
        if(self.isvar(args[0])):
            self.output += str(self.getvar(args[0])).replace("_", " ") + " "
            return 0
        elif self.isnum(args[0]):
            self.output += str(args[0])
        elif args[0] == ":":
            self.output += args[1:].replace("_", " ") + " "
        else:
            return args[0] + " is neither a name nor a value."

    # Sa3: Stores 3 in a
    def store(self, args):
        if self.isvar(args[0]):
            if self.isnum(args[1:]):
                self.setvar(args[0], int(args[1:]))
                return 0
            elif args[1] == ":":
                self.setvar(args[0], str(args[2:]))
                return 0
            else:
                return args[1] + " is not a number or string."
        else:
            return args[0] + " is not a variable."

    # Cab: Copies contents of a into b
    def copy(self, args):
        if self.isvar(args[0]):
            if self.isvar(args[1]):
                self.setvar(args[1], self.getvar(args[0]))
                return 0
            else:
                return args[1] + " is not a variable."
        else:
            return args[0] + " is not a variable."

    # MXabc: Performs math operation X on b and c and stores result in a
    def math(self, args):
        if self.isvar(args[1]) and self.isvar(args[2]) and self.isvar(args[3]):
            op = args[0]
            a = self.getvar(args[2])
            b = self.getvar(args[3])
            c = args[1]
            if op == 'A':
                self.setvar(c, a + b)
                return 0
            elif op == 'S':
                self.setvar(c, a - b)
                return 0
            elif op == 'M':
                self.setvar(c, a * b)
                return 0
            elif op == 'D':
                self.setvar(c, a / b)
                return 0
            elif op == 'E':
                self.setvar(c, a**b)
                return 0
            elif op == 'G':
                self.setvar(c, int(a > b))
                return 0
            elif op == 'L':
                self.setvar(c, int(a < b))
                return 0
            else:
                return op + " is not a known math operation."
        else:
            return "One or more of the given arguments is not a variable."

    # LaX: Performs command X, a times
    def loop(self, args):
        if self.isvar(args[0]):
            if self.isfunc(args[1]):
                for i in range(self.getvar(args[0])):
                    ret = self.exec(args[1], args[2:])
                    if isinstance(ret, str):
                        return ret
                return 0
            else:
                return args[1] + " is not a command."
        else:
            return args[0] + " is not a variable."

    # IaX: If a is nonzero, perform command X
    def ifs(self, args):
        if self.isvar(args[0]):
            if self.isfunc(args[1]):
                if self.getvar(args[0]) != 0:
                    return self.exec(args[1], args[2:])
                else:
                    return 0
            else:
                return args[1] + " is not a command."
        else:
            return args[0] + " is not a variable."

    # Ra: Resets variable a to 0.
    # RA: Resets all variables.
    def res(self, args):
        if args[0] == 'A':
            self.reset_data()
            return 0
        elif self.isvar(args[0]):
            self.setvar(args[0], 0)
            return 0
        else:
            return args[0] + " is neither a variable nor the flag A for all variables."

    # GXa: Gets input of type X (I or S) and stores it in a
    def getin(self, args):
        if self.isvar(args[1]):
            if args[0] == 'I':
                self.setvar(args[1], int(input("G$ ")))
                return 0
            elif args[0] == 'S':
                self.setvar(args[1], input("G$ "))
                return 0
            else:
                return "G should be followed by I (int) or S (string)"
        else:
            return args[1] + " is not a variable."

    # Na: If a is nonzero, set it to 0, otherwise set it to 1.
    def negate(self, args):
        if self.isvar(args[0]):
            if self.getvar(args[0]) == 0:
                self.setvar(args[0], 1)
                return 0
            else:
                self.setvar(args[0], 0)
                return 0
        else:
            return args[0] + " is not a variable."

    # BXabc: Performs boolean function X on b and c and stores result in a
    def bool(self, args):
        if self.isvar(args[1]) and self.isvar(args[2]) and self.isvar(args[3]):
            op = args[0]
            a = args[1]
            b = self.getvar(args[2])
            c = self.getvar(args[3])
            if op == 'E': # equal
                self.setvar(a, int(b == c))
            elif op == 'A': # and
                self.setvar(a, int(b and c))
            elif op == 'O': # or
                self.setvar(a, int(b or c))
            elif op == 'X': # xor
                self.setvar(a, int((b and not c) or (not b and c)))
            else:
                return op + " is not a known boolean function."

            return 0
        else:
            return "One or more of the given arguments are not variables."

    ### PARSING / EXECUTING FUNCTIONS ###

    # Separates a line into multiple commands,
    # and executes them one by one.
    def parse_exec(self):
        commands = str(self.input).split(" ")
        for command in commands:
            # Check for a comment
            if command[0] == '!':
                break
            # Run the corresponding function with the rest of the
            # string as arguments
            ret = self.exec(command[0], command[1:])
            if isinstance(ret, str):
                self.output = "ERROR in " + command + ": " + ret
                break


    # Executes a command.
    def exec(self, name, args):
        if self.isfunc(name):
            try: # Ready to catch general argument errors
                ret = self.func[name](args)
                if isinstance(ret, str):
                    return ret
                else:
                    return 0
            except IndexError:
                return "Not enough arguments"
            except ZeroDivisionError:
                return "Division by zero"
            except TypeError:
                return "Mismatched variable types"
        else:
            return "Unknown command " + name