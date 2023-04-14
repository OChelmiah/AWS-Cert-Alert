import json
import boto3
import os
from datetime import datetime, timedelta, timezone

utc = timezone.utc
# make today timezone aware
today = datetime.now().replace(tzinfo=utc)
time = datetime.now().isoformat(timespec='seconds')
now = datetime.strptime(time[0:10], '%Y-%m-%d')
sh_time = today.strftime("%Y-%m-%dT%H:%M:%S.000Z")
expiry_days = timedelta(days=45)

def lambda_handler(event, context):
    # check the expiry window before logging to Security Hub
    expiryDate = datetime.strptime(event['ExpiresOn'][0:10], '%Y-%m-%d')
    expiry = expiryDate - now
    if expiry < expiry_days:
        response = handle_single_cert(event, context.invoked_function_arn, expiry)
    else:
        response = "The current certificate does not have an upcoming expiration date"
    return {
        'statusCode': 200,
        'body': response 
    }

def handle_single_cert(event, context_arn, expiry):
    if expiry < timedelta(days=0):
        expiry = expiry*-1
        expiryType = "Expired"
        result = 'The following certificate expired ' + str(expiry) + ' days ago: ' + event['DomainName']
    else:
        result = 'The following certificate expires in ' + str(expiry) + ' days: ' + event['DomainName']
        expiryType = "Upcoming Expiry"
    log = log_finding_to_sh(event, context_arn, result, expiryType)
    result = result + ' (' + event['CertificateArn'] + ')  - ' + log
    return result
    
def log_finding_to_sh(event, context_arn, message, expiryType):
    # setup for security hub
    account = (event['CertificateArn'][22:34])
    sh_region = (event['CertificateArn'][12:21])
    sh_hub_arn = "arn:aws:securityhub:{0}:{1}:hub/default".format(sh_region, account)
    sh_product_arn = "arn:aws:securityhub:{0}:{1}:product/{1}/default".format(sh_region, account)
    # check if security hub is enabled, and if the hub arn exists
    sh_client = boto3.client('securityhub', region_name = sh_region)
    try:
        sh_enabled = sh_client.describe_hub(HubArn = sh_hub_arn)
    # the previous command throws an error indicating the hub doesn't exist or lambda doesn't have rights to it so it will stop attempting to use it
    except Exception as error:
        sh_enabled = None
        print ('Default Security Hub product doesn\'t exist')
        response = 'Security Hub disabled'
    # This is used to generate the URL to the cert in the Security Hub Findings to link directly to it
    cert_id = event['CertificateArn'][47:]
    if sh_enabled:
        # set up a new findings list
        new_findings = []
            # add expiring certificate to the new findings list
        new_findings.append({
            "SchemaVersion": "2018-10-08",
            "Id": cert_id,
            "ProductArn": sh_product_arn,
            "GeneratorId": context_arn,
            "AwsAccountId": account,
            "Types": [
                "Software and Configuration Checks/AWS Config Analysis"
            ],
            "CreatedAt": sh_time,
            "UpdatedAt": sh_time,
            "Severity": {
                "Original": '89.0',
                "Label": 'HIGH'
            },
            "Title": 'Certificate expiration',
            "Description": expiryType,
            'Remediation': {
                'Recommendation': {
                    'Text': message + '. A new certificate for ' + event['DomainName'] + ' should be imported to replace the existing imported certificate before expiration',
                    'Url': "https://console.aws.amazon.com/acm/home?region=" + sh_region + "#/?id=" + cert_id
                }
            },
            'Resources': [
                {
                    'Id': cert_id,
                    'Type': 'ACM Certificate',
                    'Partition': 'aws',
                    'Region': sh_region
                }
            ],
            'Compliance': {'Status': 'WARNING'}
        })
        # push any new findings to security hub
        if new_findings:
            try:
                response = sh_client.batch_import_findings(Findings=new_findings)
                if response['FailedCount'] > 0:
                    print("Failed to import {} findings".format(response['FailedCount']))
            except Exception as error:
                print("Error: ", error)
                raise
    return json.dumps(response)

# function to setup the sh region    
def get_sh_region(event_region):
    # security hub findings may need to go to a different region so set that here
    if os.environ.get('SECURITY_HUB_REGION') is None:
        sh_region_local = event_region
    else:
        sh_region_local = os.environ['SECURITY_HUB_REGION']
    return sh_region_local