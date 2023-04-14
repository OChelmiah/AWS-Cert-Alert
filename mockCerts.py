import json
import boto3

def lambda_handler(event, context):
    
    account = event
    
    certs = [
        {
            "CertificateArn": "arn:aws:acm:us-east-1:916507989922:certificate/certificate_ID",
            "DomainName": "example.com",
		    "SubjectAlternativeNameSummaries": [
                "example.com",
                "other.example.com"
            ],
            "HasAdditionalSubjectAlternativeNames": "false",
            "Status": "ISSUED",
            "Type": "NATIVE",
            "KeyAlgorithm": "RSA_2048",
            "SignatureAlgorithm": "sha256WithRSAEncryption",
            "KeyUsages": [
                "DIGITAL_SIGNATURE",
                "KEY_ENCIPHERMENT"
            ],
            "ExtendedKeyUsages": [
                "NONE"
            ],
            "InUse": "True",
            "RenewalEligibility": "INELIGIBLE",
            "NotBefore": "2022-06-14T23:42:49+00:00",
            "NotAfter": "2032-06-11T23:42:49+00:00",
            "CreatedAt": "2022-08-25T19:28:05.531000+00:00",
            "ImportedAt": "2022-08-25T19:28:05.544000+00:00",
            "ExpiresOn": "2024-04-26T00:00:00.000000+00:00"
        },
        {
            "CertificateArn": "arn:aws:acm:us-east-1:916507989922:certificate/certificate_ID2",
            "DomainName": "example2.com",
		    "SubjectAlternativeNameSummaries": [
                "example2.com",
                "other2.example.com"
            ],
            "HasAdditionalSubjectAlternativeNames": "false",
            "Status": "ISSUED",
            "Type": "IMPORTED",
            "KeyAlgorithm": "RSA_2048",
            "SignatureAlgorithm": "md5WithRSAEncryption",
            "KeyUsages": [
                "DIGITAL_SIGNATURE",
                "KEY_ENCIPHERMENT"
            ],
            "ExtendedKeyUsages": [
                "NONE"
            ],
            "InUse": "False",
            "RenewalEligibility": "INELIGIBLE",
            "NotBefore": "2022-06-14T23:42:49+00:00",
            "NotAfter": "2023-01-31T23:42:49+00:00",
            "CreatedAt": "2022-08-25T19:28:05.531000+00:00",
            "ImportedAt": "2022-08-25T19:28:05.544000+00:00",
            "ExpiresOn": "2023-01-31T00:00:00.000000+00:00"
        },
        {
            "CertificateArn": "arn:aws:acm:us-east-1:916507989922:certificate/certificate_ID3",
            "DomainName": "example3.com",
		    "SubjectAlternativeNameSummaries": [
                "example3.com",
                "other.example3.com"
            ],
            "HasAdditionalSubjectAlternativeNames": "false",
            "Status": "ISSUED",
            "Type": "IMPORTED",
            "KeyAlgorithm": "RSA_2048",
            "SignatureAlgorithm": "sha256WithRSAEncryption",
            "KeyUsages": [
                "DIGITAL_SIGNATURE",
                "KEY_ENCIPHERMENT"
            ],
            "ExtendedKeyUsages": [
                "NONE"
            ],
            "InUse": "False",
            "RenewalEligibility": "INELIGIBLE",
            "NotBefore": "2022-06-14T23:42:49+00:00",
            "NotAfter": "2032-06-11T23:42:49+00:00",
            "CreatedAt": "2022-08-25T19:28:05.531000+00:00",
            "ImportedAt": "2022-08-25T19:28:05.544000+00:00",
            "ExpiresOn": "2023-02-01T00:00:00.000000+00:00"
        },
        {
            "CertificateArn": "arn:aws:acm:us-east-1:916507989922:certificate/certificate_ID4",
            "DomainName": "example4.com",
		    "SubjectAlternativeNameSummaries": [
                "example4.com",
                "other.example4.com"
            ],
            "HasAdditionalSubjectAlternativeNames": "false",
            "Status": "ISSUED",
            "Type": "IMPORTED",
            "KeyAlgorithm": "EC_prime256v1",
            "SignatureAlgorithm": "ecdsa-with-SHA256",
            "KeyUsages": [
                "DIGITAL_SIGNATURE",
                "KEY_ENCIPHERMENT"
            ],
            "ExtendedKeyUsages": [
                "NONE"
            ],
            "InUse": "True",
            "RenewalEligibility": "INELIGIBLE",
            "NotBefore": "2022-06-14T23:42:49+00:00",
            "NotAfter": "2032-06-11T23:42:49+00:00",
            "CreatedAt": "2022-08-25T19:28:05.531000+00:00",
            "ImportedAt": "2022-08-25T19:28:05.544000+00:00",
            "ExpiresOn": "2024-03-01T00:00:00.000000+00:00"
        },
        {
            "CertificateArn": "arn:aws:acm:us-east-1:916507989922:certificate/certificate_ID5",
            "DomainName": "example5.com",
		    "SubjectAlternativeNameSummaries": [
                "example5.com",
                "other.example5.com"
            ],
            "HasAdditionalSubjectAlternativeNames": "false",
            "Status": "ISSUED",
            "Type": "NATIVE",
            "KeyAlgorithm": "RSA_2048",
            "SignatureAlgorithm": "sha224WithRSAEncryption",
            "KeyUsages": [
                "DIGITAL_SIGNATURE",
                "KEY_ENCIPHERMENT"
            ],
            "ExtendedKeyUsages": [
                "NONE"
            ],
            "InUse": "True",
            "RenewalEligibility": "INELIGIBLE",
            "NotBefore": "2022-06-14T23:42:49+00:00",
            "NotAfter": "2032-06-11T23:42:49+00:00",
            "CreatedAt": "2022-08-25T19:28:05.531000+00:00",
            "ImportedAt": "2022-08-25T19:28:05.544000+00:00",
            "ExpiresOn": "2023-04-20T00:00:00.000000+00:00"
        }
    ]
    
    return {
        'statusCode': 200,
        'body': certs
    }
