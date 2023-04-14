import json
import boto3
from datetime import datetime, timedelta, timezone

def lambda_handler(event,context):
    dynamodb = boto3.resource('dynamodb')
    cert = event
    
    #table name
    table = dynamodb.Table('CertAlert')
    #inserting values into table
    cert["Renewal"] = check_expiry_date(cert)
    response = table.put_item(
       Item=cert
    )
    return {
        'statusCode': 200,
        'body': response
    }
    
def check_expiry_date(cert):
    utc = timezone.utc
    # make today timezone aware
    today = datetime.now().replace(tzinfo=utc)
    time = datetime.now().isoformat(timespec='seconds')
    now = datetime.strptime(time[0:10], '%Y-%m-%d')
    expiry_days = timedelta(days=45)
    expiryDate = datetime.strptime(cert['ExpiresOn'][0:10], '%Y-%m-%d')
    expiry = expiryDate - now
    if expiry < timedelta(days=0):
        expiry = expiry*-1
        expiryType = "This certificate has expired, please renew if certificate is needed"
    elif expiry < expiry_days:
        expiryType = "Expiration date in the next 45 days, please renew"
    else:
        expiryType = "No renewal needed"
    return expiryType