import json
import boto3
from datetime import datetime, timedelta, timezone


def lambda_handler(event, context):
    regions = ["us-west-1", "us-west-2", "us-east-2", "us-east-1", "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "eu-north-1", "sa-east-1"]
    try:
        # Execute the script for all above indicated regions
        for region in regions:
            client = boto3.client('kinesis',region_name=region)
            streams = client.list_streams().get('StreamNames')
            for stream in streams:
                streamData = client.describe_stream_summary(StreamName=stream)
                
                streamName = streamData['StreamDescriptionSummary']['StreamName']
                streamDate = streamData['StreamDescriptionSummary']['StreamCreationTimestamp']

                # Expire stream after 6 hours. This can be parametrized
                expireTime = datetime.now(timezone.utc) - timedelta(hours=6)
                
                if streamDate < expireTime:
                    client.delete_stream(StreamName=stream,EnforceConsumerDeletion=True)
                        
    except Exception as e:
        print(e)
        print('Error executing this function.')
        raise e
