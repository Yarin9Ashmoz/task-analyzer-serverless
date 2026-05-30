import json
import os
import uuid
import boto3
from botocore.exceptions import ClientError

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TASKS_TABLE_NAME', 'tasks')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    AWS Lambda handler that receives task details and stores them in DynamoDB.
    """
    try:
        # Parse the incoming request body
        body = json.loads(event.get('body', '{}')) if event.get('body') else {}
        
        task_title = body.get('title')
        task_description = body.get('description', '')
        
        # Validation: Ensure title is provided
        if not task_title:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "Missing required field: title"})
            }
        
        # Create a unique task item
        new_task = {
            'id': str(uuid.uuid4()),  # Generates a random unique ID (GUID)
            'title': task_title,
            'description': task_description,
            'status': 'Pending'       # Default status for new tasks
        }
        
        # Write the item to the DynamoDB table
        table.put_item(Item=new_task)
        
        return {
            "statusCode": 201,  # Created
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Task created successfully!",
                "task": new_task
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
                "error": "Failed to save task to database",
                "details": e.response['Error']['Message']
            })
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Invalid request payload", "details": str(e)})
        }