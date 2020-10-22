""" First part with EC2 and a Python program """

def parser(msg_body):
    # input : msg body from queue
    # output : list of marks as integers
    
    marks = msg_body.split("/")
    int_marks = []
    for mark in marks:
        int_mark = int(mark)
        int_marks.append(int_mark)
    return int_marks


def process_marks(msg_body):
    # input : marks_list = marks (as float) of students
    # output : mean, median, max, min of given marks
    
    # create list of marks and sort it (for median calc)
    marks_list = parser(msg_body)
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
