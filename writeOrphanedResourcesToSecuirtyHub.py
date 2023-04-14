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
    response = check_for_orphans(event, context)
    return {
        'statusCode': 200,
        'body': response 
    }
    
def check_for_orphans(event, context):
    if event['ResourceStatus'] == "DELETE_SKIPPED":
        response = log_finding_to_sh(event, context.invoked_function_arn)
    else:
        response = "Resource successfully deleted"
    return response
    
def log_finding_to_sh(event, context_arn):
    # setup for security hub
    account = (event['StackId'][33:45])
    sh_region = (event['StackId'][23:32])
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
        
    if sh_enabled:
        # set up a new findings list
        new_findings = []
            # add expiring certificate to the new findings list
        new_findings.append({
            "SchemaVersion": "2018-10-08",
            "Id": event['PhysicalResourceId'],
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
            "Title": 'Orphaned Resource',
            "Description": 'Resouce has been orphaned and is no longer in use',
            'Remediation': {
                'Recommendation': {
                    'Text': 'The resource should be reviewed and deleted properly. If the resource is a storage container, ensure the container is empty before attemting to delete.',
                    #'Url': "https://console.aws.amazon.com/acm/home?region=" + sh_region + "#/?id=" + cert_id
                }
            },
            'Resources': [
                {
                    'Id': event['PhysicalResourceId'],
                    'Type': event['ResourceType'],
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