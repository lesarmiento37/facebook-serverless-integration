import json
import os

def generate_policy(principal_id, effect, resource):
    """Genera un documento de política IAM para API Gateway."""
    if not effect or not resource:
        return {"principalId": principal_id}

    return {
        "principalId": principal_id,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource
                }
            ]
        }
    }

def validate_token(token):
    """Valida el token de autorización contra una lista de tokens válidos."""
    valid_tokens = os.getenv("VALID_TOKENS", "xyz987").split(",")  # Admite múltiples tokens separados por coma
    return token in valid_tokens

def lambda_handler(event, context):
    """Maneja la autorización basada en el token enviado en la solicitud."""
    print("📥 Evento recibido:", json.dumps(event, indent=2))

    try:
        token = event.get("authorizationToken", "").strip()
        method_arn = event.get("methodArn", "")

        if not token or not method_arn:
            print("❌ Falta el token o el ARN del método")
            return generate_policy("user", "Deny", method_arn)

        if validate_token(token):
            print("✅ Token válido, acceso permitido")
            return generate_policy("user", "Allow", method_arn)
        else:
            print("🚫 Token inválido, acceso denegado")
            return generate_policy("user", "Deny", method_arn)

    except Exception as e:
        print("❌ Error en la autorización:", str(e))
        return generate_policy("user", "Deny", "")