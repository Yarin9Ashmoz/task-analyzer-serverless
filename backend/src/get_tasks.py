import json

def lambda_handler(event, context):
    """
    AWS Lambda handler that returns a mock list of tasks.
    This serves as the initial boilerplate for our Serverless API.
    """
    
    # Mock data to simulate database records during initial development
    mock_tasks = [
        {"id": "1", "title": "Setup GitHub Repo", "status": "Done"},
        {"id": "2", "title": "Configure AWS Lambda", "status": "In Progress"}
    ]
    
    # Return an HTTP 200 OK response with JSON payload
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            # Critical: Enable CORS to allow the frontend to safely fetch data from this API
            "Access-Control-Allow-Origin": "*"  
        },
        "body": json.dumps({
            "message": "Hello from Lambda! Tasks fetched successfully.",
            "tasks": mock_tasks
        })
    }