""" First part with EC2 and a Python program """

def process_marks(marks_list):
    # input : marks_list = list of marks (as float) of students
    # output : mean, median, max, min of given marks
    
    # sort it (for median calc)
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

    # output result : max/min/mean/median
    resultat = "Max: " + str(max_mark) + "\n"
    resultat += "Min: " + str(min_mark) + "\n"
    resultat += "Mean: " + str(mean) + "\n"
    resultat += "Median: " + str(median)
    return resultat

