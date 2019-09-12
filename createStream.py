import json
import boto3


def lambda_handler(event, context):
    
    try:
        client = boto3.client('kinesis',region_name=event['region'])
        client.create_stream(StreamName=event['streamName'],ShardCount=int(event['shardCount']))
        
    except Exception as e:
        print(e)
        print('Error executing this function.')
        raise e
