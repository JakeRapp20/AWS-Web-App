import boto3
import pprint

# Builds session with access keys is AWS CONFIGURE
session = boto3.Session(profile_name='default')

# Initializes boto3 ec2 for later use below
ec2 = boto3.client ('ec2')


def ec2_describe():
    response = ec2.describe_instances()
    instance_list = []
    for instances in response['Reservations']:
        for instance in instances['Instances']:
            instance_info = {}
            for key, value in instance.items():
                instance_info[key] = value
            instance_list.append(instance_info)

    pprint.pprint(instance_list[0]['InstanceId'])
    return instance_list

ec2_describe()
