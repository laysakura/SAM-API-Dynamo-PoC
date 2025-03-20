import os
import pytest
import boto3
from moto import mock_dynamodb


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="function")
def dynamodb(aws_credentials):
    with mock_dynamodb():
        yield boto3.resource("dynamodb", region_name="us-east-1")


@pytest.fixture(scope="function")
def users_table(dynamodb):
    table = dynamodb.create_table(
        TableName="Users",
        KeySchema=[{"AttributeName": "user_id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "user_id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )

    # Insert test data
    table.put_item(
        Item={
            "user_id": "user123",
            "name": "Test User",
            "email": "test@example.com",
            "plan": "free",
        }
    )

    table.put_item(
        Item={
            "user_id": "user456",
            "name": "Premium User",
            "email": "premium@example.com",
            "plan": "premium",
        }
    )

    return table
