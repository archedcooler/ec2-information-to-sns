#!/usr/bin/env python3

from botocore.client import Config
import boto3
    
    
def lambda_handler(event, context):
    
    config = Config(connect_timeout=5, retries={'max_attempts': 3})
    AWS_REGION = "us-east-1"
    EC2_RESOURCE = boto3.resource('ec2', region_name=AWS_REGION, config=config)
    
    #Get All EC2 Resources in VPC
    ec2_resources = EC2_RESOURCE.instances.all()
    
    #Gets instance ID from EC2 Status event from Event Bridge where status was changed to Running
    instance_id = (event["detail"]["instance-id"])
    
  
    for instance in ec2_resources:
    
        if (instance.id == instance_id):
            
            #For logging Purposes
            print(f'EC2 instance {instance.id}" information:')
            print(f'Instance state: {instance.state["Name"]}')
            print(f'Instance AMI: {instance.image.id}')
            print(f'Instance platform: {instance.platform}')
            print(f'Instance type: {instance.instance_type}')
            print(f'Private IPv4 address: {instance.private_ip_address}')
            for d in instance.tags:
                if d["Key"] == "Name":
                    # print(f'Instance Name:{d["Value"]}')
                    instance_name = d["Value"]
            print(f'Instance Name: {instance_name}')
            print('-'*60)
            
            #Messgae Details
            topic_arn = "<arn>" 
            subject = "An EC2 Has Entered Running State."
            message = f"""An EC2 instance has entered running state.\n
            Instance {instance.id} information:\n
            Instance Name: {instance_name}\n
            IP Address: {instance.private_ip_address}\n
            Instance AMI: {instance.image.id}\n
            Instance platform: {instance.platform}\n
            Instance type: {instance.instance_type}"""
            
            # Publish to topic
            sns = boto3.client("sns", region_name=AWS_REGION) 
            sns.publish(TopicArn=topic_arn, Message=message, Subject=subject)
        
            return {
                'StatusCode': 200,
                'Body': "Success"
            }

 
