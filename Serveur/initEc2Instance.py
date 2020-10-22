import boto3
import botocore
import paramiko
import time
from botocore.exceptions import ClientError

def initInstance() :
    key_pair_file_name = 'ec2-keypair'
    instance_public_dns = createEc2Instance(key_pair_file_name)
    #instance_public_dns='ec2-18-206-253-121.compute-1.amazonaws.com'
    client = connectInstance(key_pair_file_name, instance_public_dns)
    installPackets(client)
    sendPythonFiles(client)

    # Pour tester
    #stdin, stdout, stderr = client.exec_command('python3 myfile.py')
    #print("Error : %s" % stderr.read())
    #print("Out : %s" % stdout.read())
    #client.close()


def createEc2Instance(key_pair_file_name) :
    ec2_ressource = boto3.resource('ec2')
    ec2_client = boto3.client('ec2')

    vpcs = ec2_client.describe_vpcs()
    vpc_id = vpcs.get('Vpcs', [{}])[0].get('VpcId', '')
    print('VpcId= %s' % vpc_id)

    ###### Create ec2 key pair ######

    # call the boto ec2 function to create a key pair
    key_pair = ec2_ressource.create_key_pair(KeyName=key_pair_file_name)

    # create a file to store the key locally
    outfile = open(key_pair_file_name,'w')

    # capture the key and store it in a file
    KeyPairOut = str(key_pair.key_material)
    print(KeyPairOut)
    outfile.write(KeyPairOut)


    ###### Create ec2 security group ######

    try:
        response = ec2_client.create_security_group(GroupName='MySecurityGroup55',
                                            Description='My security group description',
                                            VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        print('Ingress Successfully Set %s' % data)
    except ClientError as e:
        print(e)


    ###### Create ec2 instance ######

    instances = ec2_ressource.create_instances(
        ImageId='ami-0c94855ba95c71c99',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName='ec2-keypair',
        SecurityGroupIds=[
            security_group_id
        ]
    )

    instance = instances[0]

    print('Wait until running instance ...')
    instance.wait_until_running()
    print('Wait until initializing instance ...')
    time.sleep(15)

    # Reload the instance attributes
    instance.load()

    instance_id = instance.id
    instance_public_dns = instance.public_dns_name
    print('public_dns=%s' % instance_public_dns)

    return instance_public_dns

# Penser à client.close()
def connectInstance(key_pair_file_name, instance_public_dns) :
    username = 'ec2-user'

    key = paramiko.RSAKey.from_private_key_file(key_pair_file_name)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect/ssh to an instance
    try:
        print("Try to connect to ec2 instance ...")
        client.connect(hostname=instance_public_dns, username=username, pkey=key)
        return client
    except Exception as e:
        print(e)
    

def installPackets(client) :
    print("Intalling python3 ...")
    stdin, stdout, stderr = client.exec_command('sudo yum install python3 -y')
    print("E : %s / O : %s" %(stderr.read(), stdout.read()))
    print("Intalling boto3 ...")
    stdin, stdout, stderr = client.exec_command('sudo python3 -m pip install boto3')
    print("E : %s / O : %s" %(stderr.read(), stdout.read()))
    #stdin, stdout, stderr = client.exec_command('sudo python3 -m pip install paramiko')

def sendPythonFiles(client) :
    ftp_client=client.open_sftp()
    ftp_client.put('myfile.py','myfile.py')
    ftp_client.close()

#initInstance()


