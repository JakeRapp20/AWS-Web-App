import boto3
import pprint
from flask import session



def ec2_describe():
    aws_access_key = session.get('access_key')
    aws_secret_access_key = session.get('secret_access_key')
    region = session.get('region')
    aws_session = boto3.Session(aws_access_key, aws_secret_access_key, region_name=region)
    ec2 = aws_session.client('ec2')
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

