import boto3
import json

sqs = boto3.client('sqs')
queueName = "sqs_queue"

def createPolicy():
  queuePolicy = {
    "Version": "2008-10-17",
    "Id": "__default_policy_ID",
    "Statement": [
    # {
    #   "Sid": "__owner_statement",
    #   "Effect": "Allow",
    #   "Principal": {
    #     "AWS": "*"
    #   },
    #   "Action": "SQS:*",
    #   "Resource": "arn:aws:sqs:us-east-1:319216586834:sqs_queue",
    #   "Condition": {
    #     "StringEquals": {
    #       "aws:SourceAccount": "319216586834"
    #     },
    #     "ArnLike": {
    #       "aws:SourceArn": [
    #         "arn:aws:s3:*:*:s3foreventnotification",
    #         "arn:aws:s3:*:*:tests3-storage"
    #       ]
    #     }
    #   }
    # },
    {
      "Sid": "topic-subscription",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "SQS:*",
      "Resource": "arn:aws:sqs:us-east-1:319216586834:sqs_queue",
      "Condition": {
        "ArnLike": {
          "aws:SourceArn": "arn:aws:sns:us-east-1:319216586834:Test"
        }
      }
    }
  ]}
  queue_attrs = {"Policy" : json.dumps(queuePolicy)}
  sqs.set_queue_attributes( 
    QueueUrl='https://queue.amazonaws.com/319216586834/sqs_queue',
    Attributes=queue_attrs)

def createQueue():
  sqs.create_queue(
    QueueName = queueName,
    Attributes={
        'DelaySeconds': '0',
        'MessageRetentionPeriod': '86400'
    }
  )
  createPolicy()

createQueue()


