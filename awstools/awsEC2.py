import boto3
from botocore.exceptions import ClientError

try:
    from awstools.credential import ConfigAWS
except:
    from credential import ConfigAWS


class ConfigAWS_ami():

    ami = ""  # need to add


class MemcacheEC2(object):
    def __init__(self, ec2_client):
        self.ec2_client = ec2_client
        self.maxMemcacheNumber = 8
        self.memcacheDict = {}

        self.amiID = ConfigAWS_ami.ami
