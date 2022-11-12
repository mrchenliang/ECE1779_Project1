import boto3
import botocore
from botocore.exceptions import ClientError
import os
try:
    from awstools.credential import ConfigAWS
except:
    from credential import ConfigAWS
import base64

class S3_Class(object):
    def __init__(self, s3_client):
        self.s3_client = s3_client
        self.bucketName = ""  # need to add

    def initialize_bucket(self):
        response = self.s3_client.list_buckets()['Buckets']

        name = self.bucketName
        bucketExist = False
        # print(response)
        for dict in response:
            if dict['Name'] == name:
                bucketExist = True

        if not bucketExist:
            self.s3_client.create_bucket(Bucket=name)
