import boto3

#script a faire tourner sur l'instance pour récuperer les données de la queue.

Queue_name = 'MyQueue.fifo'

sqs = boto3.resource('sqs')

try:
        queue = sqs.get_queue_by_name(QueueName= Queue_name)
        print("Queue exist yeah")
except:
        print("queue does not exist ahhhh")


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
				#message has been processed it can be  remove to process others messages
                message.delete()
