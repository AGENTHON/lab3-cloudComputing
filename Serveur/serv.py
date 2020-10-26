import boto3


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






#script a faire tourner sur l'instance pour récuperer les données de la queue.



sqs = boto3.resource('sqs')

try:
        queue = sqs.get_queue_by_name(QueueName= "requestQueue.fifo")
        print("Queue exist yeah")
        
        #Récupération et traitement des info en continu
        while 1 :
            # Process messages by printing out body and optional author name
            for message in queue.receive_messages(MessageAttributeNames=['Author']):
                # Get the custom author message attribute if it was set
                author_text = ''
                if message.message_attributes is not None:
                    author_name = message.message_attributes.get('Author').get('StringValue')
                    if author_name:
                        author_text = ' ({0})'.format(author_name)

                # Print out the body and author (if set)
                print('MESSAGE , {0}{1}'.format(message.body, author_text))
                
                #calcul du resultat
                result = process_marks(message.body)
                #message has been processed it can be  remove to process others messages
                message.delete()
                
                #renvoyer  le resultat :
                
                #création d'une nouvelle queue :
                Rqueue = sqs.create_queue(QueueName="responseQueue.fifo", Attributes={'FifoQueue': 'true', 'DelaySeconds': '5', 'ContentBasedDeduplication': 'true'})
                
                #envoi du message
                response = Rqueue.send_message(MessageBody=result, MessageGroupId='messages')
                

except:
        print("queue not found ahhhh")


