import json

def generate_policy(principal_id, effect, resource):
    """Generate an IAM policy document"""
    auth_response = {
        "principalId": principal_id
    }

    if effect and resource:
        policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource
                }
            ]
        }
        auth_response["policyDocument"] = policy_document

    return auth_response

def lambda_handler(event, context):
    """Handle incoming request and authorize based on token"""
    token = event["authorizationToken"]

    # Replace this with your token validation logic
    valid_token = "xyz987"

    if token == valid_token:
        return generate_policy("user", "Allow", event["methodArn"])
    else:
        return generate_policy("user", "Deny", event["methodArn"])
