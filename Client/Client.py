import boto3
import initEc2Instance
import initQueues


# Create requestQueue and responseQueue
requestQueue, responseQueue = initQueues.initQueues()

# Create EC2 instance (with key-pair ans security group)
# Install all necessary packages
# Send EC2 worker's python files on instance
# Run EC2 worker on instance
initEc2Instance.initInstance()


# Client part
# This script ask some integers from console to user. Ex : 78 65 12 32
# Then it parse those integers and format them in new string like : "78/65/12/32"
# Finally it send this string in queue created before
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
response = requestQueue.send_message(MessageBody=string, MessageGroupId='messages')