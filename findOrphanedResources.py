import json
import boto3

def lambda_handler(event, context):
    result = scan_stack(event, context)
    return {
        'statusCode': 200,
        'body': result
    }

def scan_stack(event, context):
    cf_client = boto3.client('cloudformation')
    response = cf_client.describe_stack_resources(
        StackName=event['StackId'],
    )
    stack = response['StackResources']
    for resource in stack:
        for item in resource:
            resource[item] = str(resource[item])
    return stack