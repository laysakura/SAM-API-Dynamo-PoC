import json
import os
import pytest
from unittest.mock import patch, MagicMock

# Set environment variables for testing
os.environ["DYNAMODB_TABLE"] = "Users"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

from src.app import get_user


@pytest.fixture
def api_gateway_event():
    return {
        "requestContext": {"authorizer": {"principalId": "user123"}},
        "queryStringParameters": None,
    }


@pytest.fixture
def query_param_event():
    return {"requestContext": {}, "queryStringParameters": {"user_id": "user123"}}


@pytest.fixture
def lambda_context():
    return MagicMock()


def test_get_user_success(api_gateway_event, lambda_context):
    mock_user = {"user_id": "user123", "name": "Test User", "email": "test@example.com"}

    with patch("src.app.get_user_by_id", return_value=mock_user):
        response = get_user(api_gateway_event, lambda_context)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == mock_user


def test_get_user_from_query_param(query_param_event, lambda_context):
    mock_user = {"user_id": "user123", "name": "Test User", "email": "test@example.com"}

    with patch("src.app.get_user_by_id", return_value=mock_user):
        response = get_user(query_param_event, lambda_context)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == mock_user


def test_get_user_not_found(api_gateway_event, lambda_context):
    with patch("src.app.get_user_by_id", return_value=None):
        response = get_user(api_gateway_event, lambda_context)

    assert response["statusCode"] == 404
    assert "error" in json.loads(response["body"])


def test_get_user_missing_id(lambda_context):
    event = {"requestContext": {}, "queryStringParameters": None}
    response = get_user(event, lambda_context)

    assert response["statusCode"] == 400
    assert "error" in json.loads(response["body"])


def test_get_user_exception(api_gateway_event, lambda_context):
    with patch("src.app.get_user_by_id", side_effect=Exception("Test error")):
        response = get_user(api_gateway_event, lambda_context)

    assert response["statusCode"] == 500
    assert "error" in json.loads(response["body"])
