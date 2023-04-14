import json
import boto3

def lambda_handler(event,context):
    dynamodb = boto3.resource('dynamodb')
    resources = event
    #table name
    table = dynamodb.Table('OrphanedResources')
    #inserting values into table
    response = table.put_item(
       Item=resources
    )
    return {
        'statusCode': 200,
        'body': response
    }
