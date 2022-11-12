import time
import datetime
from dateutil.tz import tzutc
import boto3
from awstools.credential import ConfigAWS


class CloudwatchAPI(object):

    def __init__(self, aws_access_key_id, aws_secret_access_key):
        self.client = boto3.client('cloudwatch',
                                   region_name='us-east-1',
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key)

    def createCloudwatchClient(aws_access_key_id, aws_secret_access_key):
        '''
        Generate a cloudwatch client.
        Use __init__ instead.
        '''
        return
