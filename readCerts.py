import json
import boto3

def lambda_handler(event, context):
    
    account = event
    
    certs = [
        {
            "CertificateArn": ,
            "DomainName": ,
		    "SubjectAlternativeNameSummaries": [
                
            ],
            "HasAdditionalSubjectAlternativeNames": ,
            "Status": ,
            "Type": ,
            "KeyAlgorithm": ,
            "KeyUsages": [
                "DIGITAL_SIGNATURE",
                "KEY_ENCIPHERMENT"
            ],
            "ExtendedKeyUsages": [
                "NONE"
            ],
            "InUse": ,
            "RenewalEligibility": ,
            "NotBefore": ,
            "NotAfter": ,
            "CreatedAt": ,
            "ImportedAt": 
        }
    ]
    
    return {
        'statusCode': 200,
        'body': certs
    }
