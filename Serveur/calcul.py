""" First part with EC2 and a Python program """
import sys

def process_marks(*args):
    # input : marks_list = marks (as float) of students
    # output : mean, median, max, min of given marks
    
    # raise an error if no marks were given
    if len(args) == 0:
        print("FunctionError: Not enough marks were given")
        sys.exit(1)
    
    # create list of marks and sort it (for median calc)
    marks_list = []
    for mark in args:
        marks_list.append(mark)
    marks_list.sort()

    # maximum mark
    max_mark = marks_list[-1]

    # minimum mark
    min_mark = marks_list[0]

    # mean of marks
    mean = sum(marks_list) / len(marks_list)

    # median of marks - Python supports negative list index
    mid = len(marks_list) // 2
    median = (marks_list[mid] + marks_list[~mid]) / 2

    # output result
    print( "Maximum mark: " + str(max_mark) )
    print( "Minimum mark: " + str(min_mark) )
    print( "Mean of marks: " + str(mean) )
    print( "Median of marks: " + str(median) )


""" Tests """


# process_marks() renvoie une erreur custom

process_marks(7, 4, 15)

print("")

process_marks(8, 9, 10, 17, 8, 20, 20, 9)
