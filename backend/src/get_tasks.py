import json
import os
import boto3
from botocore.exceptions import ClientError

# Initialize the DynamoDB client using boto3
dynamodb = boto3.resource('dynamodb')

# Get the table name from environment variables (configured later in AWS)
TABLE_NAME = os.environ.get('TASKS_TABLE_NAME', 'tasks')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    AWS Lambda handler that fetches all tasks from the DynamoDB table.
    """
    try:
        # Perform a scan operation to fetch all items from the table
        response = table.scan()
        tasks = response.get('Items', [])
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"  # Required for frontend CORS integration
            },
            "body": json.dumps({
                "tasks": tasks
            })
        }
        
    except ClientError as e:
        print(f"DynamoDB Error: {e.response['Error']['Message']}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "error": "Failed to fetch tasks from database",
                "details": e.response['Error']['Message']
            })
        }