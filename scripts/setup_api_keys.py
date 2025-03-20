#!/usr/bin/env python
import os
import json
import boto3

# For local development, this script simulates API key creation
# In a real environment, this would use AWS CLI to create API keys
# and link them to user IDs in the authorization system


def create_local_api_keys():
    """Create local API key mappings for development"""
    api_keys = {
        "user123": "api-key-free-user-123",
        "user456": "api-key-premium-user-456",
        "user789": "api-key-enterprise-user-789",
    }

    # Save to local file for reference
    with open("api_keys.json", "w") as f:
        json.dump(api_keys, f, indent=2)

    print("Local API keys created and saved to api_keys.json")
    print("\nIn a production environment, you would use AWS CLI to create API keys:")
    print(
        "aws apigateway create-api-key --name 'User123Key' --enabled --value 'api-key-free-user-123'"
    )
    print(
        "aws apigateway create-usage-plan-key --usage-plan-id <usage-plan-id> --key-id <key-id> --key-type 'API_KEY'"
    )

    print("\nFor testing, use the following curl command:")
    print("curl -H 'x-api-key: api-key-free-user-123' http://localhost:3000/users")
    print("\nOr, for local development without API key validation:")
    print("curl http://localhost:3000/users?user_id=user123")


def main():
    """Main function to setup API keys"""
    create_local_api_keys()
    print("API key setup complete!")


if __name__ == "__main__":
    main()
