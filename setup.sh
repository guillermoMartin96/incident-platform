#!/bin/bash
curl -X 'POST' \
  'http://127.0.0.1:8000/incidents' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "service": "memo",
  "severity": "low",
  "description": "wants to stop this"
}'

curl -X 'POST' \
  'http://127.0.0.1:8000/incidents' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "service": "memo",
  "severity": "medium",
  "description": "getting hungry"
}'

curl -X 'POST' \
  'http://127.0.0.1:8000/incidents' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "service": "memo",
  "severity": "high",
  "description": "needs to keep working"
}'
