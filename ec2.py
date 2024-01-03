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

def backend_ec2_stop(instance_ids):
    aws_access_key = session.get('access_key')
    aws_secret_access_key = session.get('secret_access_key')
    region = session.get('region')
    aws_session = boto3.Session(aws_access_key, aws_secret_access_key, region_name=region)
    ec2 = aws_session.client('ec2')
    instances_to_stop = []
    instances_to_stop.append(instance_ids)

    stop_status_response = ec2.stop_instances(InstanceIds=instances_to_stop )
    print(instances_to_stop)
    return stop_status_response

def backend_ec2_start(instance_ids):
    aws_access_key = session.get('access_key')
    aws_secret_access_key = session.get('secret_access_key')
    region = session.get('region')
    aws_session = boto3.Session(aws_access_key, aws_secret_access_key, region_name=region)
    ec2 = aws_session.client('ec2')
    print(instance_ids)
    instances_to_start = []
    instances_to_start.append(instance_ids)

    start_status_response = ec2.start_instances(InstanceIds=instances_to_start)
    print(instances_to_start)
    return start_status_response


