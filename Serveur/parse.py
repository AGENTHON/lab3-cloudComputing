""" Parser Example """
import sys

def parse(input):
    # input is a string
    # output is a list of floats

    liste = input.split("/")
    list_marks = []
    for mark in liste:
        try:
            float_mark = float(mark)
            list_marks.append(float_mark)
        except ValueError:
            print("FunctionError: Non-Float Argument")
            sys.exit(1)
    
    return list_marks


print( parse("6/12/17/2.5/18.3") )
print("")
print( parse("6.2/12/13/15/20/a") )

