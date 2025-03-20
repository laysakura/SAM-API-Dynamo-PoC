#!/usr/bin/env python
import os
import time
import boto3
from botocore.exceptions import ClientError

# DynamoDB setup
endpoint_url = os.environ.get("AWS_ENDPOINT_URL", "http://localhost:8000")
dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint_url)
table_name = os.environ.get("DYNAMODB_TABLE", "Users")


def create_users_table():
    """Create the Users table if it doesn't exist"""
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": "user_id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "user_id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        print(f"Creating table {table_name}...")
        table.meta.client.get_waiter("table_exists").wait(TableName=table_name)
        print(f"Table {table_name} created successfully!")
        return table
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            print(f"Table {table_name} already exists.")
            return dynamodb.Table(table_name)
        else:
            print(f"Error creating table: {e}")
            raise


def seed_user_data(table):
    """Seed the Users table with sample data"""
    sample_users = [
        {
            "user_id": "user123",
            "name": "Test User",
            "email": "test@example.com",
            "plan": "free",
            "created_at": "2025-03-21",
        },
        {
            "user_id": "user456",
            "name": "Premium User",
            "email": "premium@example.com",
            "plan": "premium",
            "created_at": "2025-03-21",
        },
        {
            "user_id": "user789",
            "name": "Enterprise User",
            "email": "enterprise@example.com",
            "plan": "enterprise",
            "created_at": "2025-03-21",
        },
    ]

    with table.batch_writer() as batch:
        for user in sample_users:
            batch.put_item(Item=user)
            print(f"Added user: {user['name']} ({user['user_id']})")


def main():
    """Main function to create table and seed data"""
    # Wait for DynamoDB to be available
    max_retries = 10
    retry_count = 0

    while retry_count < max_retries:
        try:
            # Check if DynamoDB is available by listing tables
            dynamodb.meta.client.list_tables()
            break
        except Exception as e:
            print(
                f"Waiting for DynamoDB to be available... (retry {retry_count + 1}/{max_retries})"
            )
            retry_count += 1
            time.sleep(2)

    if retry_count == max_retries:
        print("Failed to connect to DynamoDB. Exiting.")
        return

    table = create_users_table()
    seed_user_data(table)
    print("Database setup complete!")


if __name__ == "__main__":
    main()
