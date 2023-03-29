import json
import boto3
import os
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    support_level = SupportLevel()
    tag_to_add = support_level.get_service_level(event)
    event['tag'] = tag_to_add
    return event

class SupportLevel:
    def __init__(self):
        self.table      = os.environ['TableName']
        self.client     = boto3.client('dynamodb')

    def get_service_level(self, event):
        domain = event['full_url'].replace('http://', '').replace('/', '').replace('https://', '')
        key = {'Domain': {'S': domain}}
        try:
            response = self.client.get_item(
                TableName   =   self.table,
                Key         =   key
                )
            if 'Item' in response:
                if response['Item']['Out-of-hours']['BOOL'] == True:
                    return '247Alarm'
                elif response['Item']['Out-of-hours']['BOOL'] == False:
                    return 'InHours'
                else:
                    raise Exception("Item not found")
            else:
                raise Exception("Item not found")
        except ClientError as e:
            print(e.response['Error']['Message'])
