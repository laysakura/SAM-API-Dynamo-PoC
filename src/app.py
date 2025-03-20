import json
import os
from typing import Dict, Any, Optional

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from db import get_user_by_id

# Initialize logger
logger = Logger()

# Initialize DynamoDB client
endpoint_url = os.environ.get('AWS_ENDPOINT_URL')
dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
table_name = os.environ.get('DYNAMODB_TABLE', 'Users')
table = dynamodb.Table(table_name)

@logger.inject_lambda_context
def get_user(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """
    Lambda handler to get user information by user_id from API key.
    
    Args:
        event: API Gateway Lambda proxy event
        context: Lambda context
    
    Returns:
        API Gateway Lambda proxy response
    """
    logger.info("Received request", extra={"event": event})
    
    try:
        # Extract user_id from the request context (API Key)
        authorizer = event.get('requestContext', {}).get('authorizer', {})
        user_id = authorizer.get('principalId')
        
        # For local testing, support query parameter
        if not user_id and event.get('queryStringParameters'):
            user_id = event.get('queryStringParameters', {}).get('user_id')
        
        if not user_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing user_id'})
            }
        
        # Get user from DynamoDB
        user = get_user_by_id(table, user_id)
        
        if not user:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': f'User with ID {user_id} not found'})
            }
        
        # Return user information
        return {
            'statusCode': 200,
            'body': json.dumps(user)
        }
    
    except Exception as e:
        logger.exception("Error processing request")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
