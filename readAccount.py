import json

def lambda_handler(event, context):

    aws_account_id = context.invoked_function_arn.split(":")[4]

   # print(aws_account_id)
    return {
        'statusCode': 200,
        'body': aws_account_id
    }
