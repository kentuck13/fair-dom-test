import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://dynamodb:8000')
