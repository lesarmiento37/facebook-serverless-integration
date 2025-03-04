import json

def lambda_handler(event, context):
    """Función Lambda Authorizer para validar el token"""
    token = event['headers'].get('Authorization')

    if token == "token_1234":
        # El token es válido
        return {
            "principalId": "user|a1b2c3d4",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": "execute-api:Invoke",
                        "Resource": event["methodArn"]
                    }
                ]
            }
        }
    else:
        # El token no es válido
        return {
            "statusCode": 403,
            "body": json.dumps({"message": "Forbidden"})
        }
