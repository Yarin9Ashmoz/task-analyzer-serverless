import json

def lambda_handler(event, context):
    """
    AWS Lambda handler that simulates creating a new task.
    This will later integrate with AWS DynamoDB to persist data.
    """
    try:
        # Check if the event body exists and parse it
        # (When API Gateway forwards a request, the payload arrives as a string in event['body'])
        if event.get("body"):
            body = json.loads(event["body"])
        else:
            body = {}

        # Extract task details from the request payload
        task_title = body.get("title", "Untitled Task")
        task_description = body.get("description", "")

        # Simulate generating a response for a newly created task
        created_task = {
            "id": "101",  # Mock ID for now
            "title": task_title,
            "description": task_description,
            "status": "Pending"
        }

        return {
            "statusCode": 201,  # 201 Created is the standard HTTP status for successful creation
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"  # CORS configuration for frontend integration
            },
            "body": json.dumps({
                "message": "Task created successfully!",
                "task": created_task
            })
        }

    except Exception as e:
        # Simple error handling for now
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "error": "Invalid request format",
                "details": str(e)
            })
        }