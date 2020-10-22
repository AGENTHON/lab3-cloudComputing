import boto3
import botocore
import pydivert
from botocore.exceptions import ClientError

ec2_ressource = boto3.resource('ec2')
ec2_client = boto3.client('ec2')

vpcs = ec2_client.describe_vpcs()
vpc_id = vpcs.get('Vpcs', [{}])[0].get('VpcId', '')
print('VpcId= %s' % vpc_id)

###### Create ec2 key pair ######

# call the boto ec2 function to create a key pair
key_pair = ec2_ressource.create_key_pair(KeyName='ec2-keypair')

# create a file to store the key locally
outfile = open('ec2-keypair.pem','w')

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

instance_id = instances[0].id
print('New instance created, instance_id=%s' % instance_id)