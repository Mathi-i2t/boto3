import boto3
import os
import json

s3 = boto3.client('s3')
bucket_name = "s3foreventnotification"

s3.create_bucket(Bucket = bucket_name)

# list all buckets
# bucketsList = s3client.list_buckets()
# print(bucketsList)

# uploading files

# buckets = s3.list_buckets()

# print(buckets)

# for bucket in buckets['Buckets']:
#     print(f'{bucket["Name"]}')


# file = f'{os.getcwd()}/demo.txt'

# print(file)

# if os.path.isfile(file):
#     print("File Exist")
#     with open(file) as fl:
#         content = fl.read()
#     fl.close()

# data = open('demo.txt', 'rb') 
# s3.Bucket('boto3fors3storagedemo').put_object(Key = 'demo.txt', Body = data)

def uploadfiles(filename, bucket, object=None):

    if object == None:
        object = filename
    
    s3 = boto3.client('s3')
    s3.upload_file(filename, bucket, object)


# with open('demo.txt', 'rb') as filename:
#     uploadfiles(filename, 'boto3fors3storage')

# uploadfiles('demo.txt', 'boto3fors3storage')

#access policy for bucket
bucket_policy = {
    'Version': '2012-10-17',
    'Statement': [{
        'Sid': 'AddPermissions',
        'Effect': 'Allow',
        'Principal': '*',
        'Action': ['*'],
        'Resource': f'arn:aws:s3:::{bucket_name}/*'
    }]
}

bucket_policy = json.dumps(bucket_policy)
s3.put_bucket_policy(Bucket = bucket_name, Policy = bucket_policy)

s3_service = boto3.resource('s3')
bucket_notification = s3_service.BucketNotification(bucket_name)

bucket_notification.put(
    NotificationConfiguration={
        'TopicConfigurations': [
            {
                'TopicArn': 'arn:aws:sns:us-east-1:319216586834:Test',
                'Events': [
                    's3:ObjectCreated:*','s3:ObjectRemoved:*'
                ]
            }
        ],
        # 'QueueConfigurations': [
        #     {
        #         'QueueArn': 'arn:aws:sqs:us-east-1:319216586834:sqs_queue',
        #         'Events': [
        #             's3:ObjectCreated:*','s3:ObjectRemoved:*'
        #         ]               
        #     }
        # ]
    },
    SkipDestinationValidation=True
)
