AWS Cert Alert is a certificate management system designed to automate and streamline the process of managing certificates, resources, and CloudFormation stacks within AWS accounts. The system utilizes a state machine with Lambda code to gather information about certificates in use, log expiring certificates in Security Hub, pass certificate details to a DynamoDB database, update a dashboard created with QuickSight Dashboard, and notify users of updates via email using Simple Notification Service.

To set up the system, simply follow these steps:
1. Set up and log into your AWS account.
2. Copy and paste the python files into individual Lambda functions.
3. Create a new state machine in Step Functions and copy the StateMachine.json into the json editor.
4. Set the state machine to run on a schedule using Event Bridge.
5. Create an SNS topic called CertAlert and assign any email addresses that need to be notified by the system.
6. Creat DynamoDB tables called CertAlert and OrphanedResources.
7. Enable Security Hub.
8. Access the sample dashboard at https://us-east-1.quicksight.aws.amazon.com/sn/accounts/916507989922/dashboards/a57c0d4a-b5e0-45ca-a07a-8855dead939f?directory_alias=certalertdashboard and click the save as button to generate a new analyses based on your data.

You can view a video guide to setting up and using the system at https://youtu.be/rfPmh9j2EuQ and you can view the website for the project at https://showcase.itcarlow.ie/
