import json

def lambda_handler(event, context):
    token = json.loads(event['authorizationToken'])
    
        
    if token == 'allow':
        print('authorized')
        response = generatePolicy('user', 'Allow', event['methodArn'])
    elif token == 'deny':
        print('unauthorized')
        response = generatePolicy('user', 'Deny', event['methodArn'])
    elif token == 'unauthorized':
        print('unauthorized')
        # Provoca un 401 Unauthorized
        raise Exception('Unauthorized')
    else:
        # Cualquier otro valor => 500 Internal Server Error
        print('Internal Error')
        raise Exception('Internal server error')
    
    # Devuelve la política en forma de dict
    return json.loads(response)

def generatePolicy(principalId, effect, resource):
    policyDocument = {
        'Version': '2012-10-17',
        'Statement': []
    }

    statementOne = {
        'Action': 'execute-api:Invoke',
        'Effect': effect,
        'Resource': resource
    }
    policyDocument['Statement'].append(statementOne)

    authResponse = {
        'principalId': principalId,
        'policyDocument': policyDocument,
        # Esto se inyecta en requestContext.authorizer en el backend
        'context': {
            "stringKey": "stringval",
            "numberKey": 123,
            "booleanKey": True
        }
    }

    return json.dumps(authResponse)
