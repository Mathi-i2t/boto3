import boto3
import json

sns = boto3.client('sns')

sns.create_topic(Name='Test')
topic = 'arn:aws:sns:us-east-1:319216586834:Test'
protocolForMail = 'email'
mailId = 'mathivanan.arulsamy@ideas2it.com'
protocolForMobileNumber = 'sms'
mobileNumber = '+918072149302'
protocolForSQS = 'sqs'
sqs_arn = 'arn:aws:sqs:us-east-1:319216586834:sqs_queue'

def subscribe(topic, protocol, endpoint):
    subscription = sns.subscribe(
        TopicArn = topic,
        Protocol = protocol,
        Endpoint = endpoint,
        ReturnSubscriptionArn = True)
    createPolicy()
    return subscription['SubscriptionArn']
    
responseForMail = subscribe(topic, protocolForMail, mailId)
responseForMobileNumber = subscribe(topic, protocolForMobileNumber, mobileNumber)
responseForSQS = subscribe(topic, protocolForSQS, sqs_arn)
print("Subscribed to a topic successfully \n Subscription arn - " + responseForMail)
print("Subscribed to a topic successfully \n Subscription arn - " + responseForMobileNumber)
print("Subscribed to a topic successfully \n Subscription arn - " + responseForSQS)

def createPolicy():
  snsPolicy = {
  "Version": "2008-10-17",
  "Id": "__default_policy_ID",
  "Statement": [
    {
      "Sid": "__default_statement_ID",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": [
        "SNS:GetTopicAttributes",
        "SNS:SetTopicAttributes",
        "SNS:AddPermission",
        "SNS:RemovePermission",
        "SNS:DeleteTopic",
        "SNS:Subscribe",
        "SNS:ListSubscriptionsByTopic",
        "SNS:Publish"
      ],
      "Resource": "arn:aws:sns:us-east-1:319216586834:Test",
      "Condition": {
        "StringEquals": {
          "aws:SourceAccount": "319216586834"
        },
        "ArnLike": {
          "aws:SourceArn": "arn:aws:s3:*:*:s3foreventnotification"
        }
      }
    }
  ]}
  sns_attr_value = json.dumps(snsPolicy)
  sns.set_topic_attributes(
    TopicArn="arn:aws:sns:us-east-1:319216586834:Test",
    AttributeName='Policy',
    AttributeValue=sns_attr_value)
