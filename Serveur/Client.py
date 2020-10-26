import boto3

# This script create a new queue if it does not exist
# This script ask some integers from console to user. Ex : 78 65 12 32
# Then it parse those integers and format them in new string like : "78/65/12/32"
# Finally it send this string in queue created before

QUEUE_NAME = 'requestQueue.fifo'

# Get the service resource
sqs = boto3.resource('sqs')
    
try:
    # Get queue by name
    queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
except:
    # If queue does not exist, create one (we use FIFO queue here)
    queue = sqs.create_queue(QueueName=QUEUE_NAME, Attributes={'FifoQueue': 'true', 'DelaySeconds': '5', 'ContentBasedDeduplication': 'true'})



myInput = input("Enter integers (separate by space): ")    # Ask integer to user
fields = myInput.split(" ")             # Split integers by space

integers = []                                           # Parse integers from string
for field in fields:                                    #
    try:                                                #
        i = int(field)                                  #
        integers.append(i)                              #
    except ValueError:                                  #
        print("'"+field+"' is not a valid integer")     #

print("Valid Integers are = "+str(integers))

string = ""                                             # Build string that will be sent to queue
for integer in integers:                                # ex : '78/23/56'
    string = string + str(integer) + "/"                #
string = string[:-1]                                    #

print("Sending='"+string+"'")
response = queue.send_message(MessageBody=string, MessageGroupId='messages')