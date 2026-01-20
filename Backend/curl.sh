#! /usr/bin/env bash

set -e

echo "Testing API"
echo -e "\nLogging in"
curl -X POST "http://localhost:8080/login" -H 'Content-Type: application/json'\
 -H 'Accept: application/json'\
 -d '{"username": "user1", "password": "pass1"}'

echo -e "\n\nCheck account in"
curl -X GET "http://localhost:8080/accounts" -H 'Content-Type: application/json'\
 -H 'Accept: application/json'\
 -H 'Authorization: token-user1'

echo -e "\n\nMake transfer" 
curl -X POST "http://localhost:8080/transfer" -H 'Content-Type: application/json'\
 -H 'Accept: application/json'\
 -H 'Authorization: token-user1'\
 -d '{"from_account": 1, "to_account": 2, "amount": 100.0}'
echo ""
