import json
import boto3
from datetime import date, datetime

def lambda_handler(event, context):
    result = get_stacks(event, context)
    return {
        'statusCode': 200,
        'body': result
        #'body': json.dumps(result, default=str)
    }
    
def get_stacks(event, context):
    cf_client = boto3.client('cloudformation')
    response = cf_client.list_stacks()
    stacks = response['StackSummaries']
    for stack in stacks:
        for resource in stack:
            stack[resource] = str(stack[resource])
    return stacks