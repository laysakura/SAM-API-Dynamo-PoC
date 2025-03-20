from typing import Dict, Any, Optional
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


def get_user_by_id(table, user_id: str) -> Optional[Dict[str, Any]]:
    """
    Get user information from DynamoDB by user_id.

    Args:
        table: DynamoDB table resource
        user_id: User ID to retrieve

    Returns:
        User information or None if not found
    """
    try:
        response = table.get_item(Key={"user_id": user_id})
        return response.get("Item")
    except ClientError as e:
        print(f"Error getting user: {e}")
        return None
