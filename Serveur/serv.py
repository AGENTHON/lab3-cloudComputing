import boto3
import sys
import os, datetime

""" Create log file for AWS bucket """


def create_log_txt(liste, result):
    # Entrees :
    # liste = les notes en format "1/3/5/7/9"
    # result = la sortie raw_result de process_marks()
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    liste = liste.replace("/", " ")
    # timestamp
    ts = str(datetime.datetime.now().timestamp()).replace('.','_')
    # nom du fichier
    log_name="log"+ts+".txt"
    fichier_log = open(log_name, "w")
    fichier_log.write(now + "\n")
    fichier_log.write(liste + "\n")
    fichier_log.write(result + "\n")
    fichier_log.close()
    # ajout du log dans le bucket
    s3_cli = boto3.client('s3')
    s3_cli.upload_file(log_name, "logs1684237", log_name)


def delete_log_txt():
    os.remove("fichier_log.txt")

#Parse an input as number separated by / as a list
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
    
    # output raw_result
    raw_result = "Max: " + str(max_mark) + " Min: " + str(min_mark) + " Mean: " + str(mean) + " Median: " + str(median)
    
    # return strings
    return [resultat, raw_result]




#script a faire tourner sur l'instance pour recuperer les donnees de la queue.



sqs = boto3.resource('sqs')

try:
    queue = sqs.get_queue_by_name(QueueName= "requestQueue.fifo")
    print("Queue exist yeah")

except:
    print("queue not found ahhhh")
    
    
    
#Recuperation et traitement des info en continu
while 1 :
# Process messages by printing out body and optional author name
    for message in queue.receive_messages(MessageAttributeNames=['Author']):
    # Get the custom author message attribute if it was set
        author_text = ''
        if message.message_attributes is not None:
            author_name = message.message_attributes.get('Author').get('StringValue')
            if author_name:
                author_text = ' ({0})'.format(author_name)

        #calcul du resultat
        result = process_marks(parse(message.body))

        # affichage du resultat
        print('MESSAGE , {0} \n {1}'.format(message.body, result[0]))
           
        #Creation des logs
        create_log_txt(message.body, result[1])
           
        #message has been processed it can be  remove to process others messages
        message.delete()
            
        #renvoyer  le resultat :
            
        #création d'une nouvelle queue :
        Rqueue = sqs.get_queue_by_name(QueueName="responseQueue.fifo")
            
        #envoi du message
        response = Rqueue.send_message(MessageBody=result[0], MessageGroupId='messages')
            


