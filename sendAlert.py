import json
import boto3

def lambda_handler(event, context):

    client = boto3.client('sns')
    snsArn = 'arn:aws:sns:us-east-1:916507989922:AWSCertAlert'
    message = "Dear User,\nThe AWS Cert Alert Dashboard has been updated. Please check the dashboard using the following link:\nhttps://us-east-1.quicksight.aws.amazon.com/sn/dashboards/a57c0d4a-b5e0-45ca-a07a-8855dead939f"

    response = client.publish(
        TopicArn = snsArn,
        Message = message ,
        Subject='AWS Cert Alert Dashboard has been updated'
    )
    
    return {
        'statusCode': 200,
        'body': response
    }
