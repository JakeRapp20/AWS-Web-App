import boto3
import pprint

# Builds session with access keys is AWS CONFIGURE
session = boto3.Session(profile_name='default')

# Initializes boto3 ec2 for later use below
ec2 = boto3.client ('ec2')


def ec2_describe():
    response = ec2.describe_instances()
    # breaking down response so list is easier to interate through on templates and routes
    instance_list = []
    for instances in response['Reservations']:
        for instance in instances['Instances']:
            instance_info = {}
            for key, value in instance.items():
                instance_info[key] = value
            instance_list.append(instance_info)

    return instance_list

def instance_details():
    # using brokendown list from ec2_describe fucntion
    instance_list = ec2_describe()
    
    return instance_list

