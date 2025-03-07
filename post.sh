#!/bin/bash
curl -X POST "https://zhh86kffoi.execute-api.us-east-1.amazonaws.com/test/webhook" \
-H "Content-Type: application/json" \
-H "Authorization: xyz987" \
-d '{"mensaje":"Hola test 2"}'

curl -X POST "https://zhh86kffoi.execute-api.us-east-1.amazonaws.com/test/prueba" \
-H "Content-Type: application/json" \
-H "Authorization: xyz987" \
-d '{"mensaje":"Hola test 2"}'


curl -X GET "https://zhh86kffoi.execute-api.us-east-1.amazonaws.com/test/prueba" \
-H "Content-Type: application/json" \
-H "Authorization: xyz987"




