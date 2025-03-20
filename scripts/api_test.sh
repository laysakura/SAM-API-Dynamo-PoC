#!/bin/bash

# Test API with API key (simulated authorizer)
echo "Testing API with user123:"
curl -s -H "x-api-key: api-key-free-user-123" http://localhost:3000/users | jq

# Test API with query parameter (for local development)
echo -e "\nTesting API with query parameter:"
curl -s "http://localhost:3000/users?user_id=user456" | jq

# Test API with non-existent user
echo -e "\nTesting API with non-existent user:"
curl -s "http://localhost:3000/users?user_id=nonexistent" | jq
