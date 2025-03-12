import json
import os

def generate_policy(principal_id, effect, method_arn):
    """Genera una política IAM para API Gateway, permitiendo todas las rutas del API."""
    if not effect or not method_arn:
        return {"principalId": principal_id}

    # Extraer el ARN base para permitir acceso a toda la API
    arn_parts = method_arn.split("/")
    api_arn = "/".join(arn_parts[:2]) + "/*"

    return {
        "principalId": principal_id,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": api_arn  # Permitir acceso a toda la API
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
    print("📥 Evento recibido authorizer:", json.dumps(event, separators=(',', ':')))

    try:
        method_arn = event.get("methodArn", "")
        token = event.get("authorizationToken", "").strip()

        # ⚡ EXCEPCIÓN para permitir solicitudes GET de verificación de Facebook
        if "hub.mode" in event.get("queryStringParameters", {}):
            print("🔹 Permitiendo verificación de Facebook sin autorización")
            return generate_policy("facebook", "Allow", method_arn)

        print(f"📢 Token recibido: {token}")
        print(f"🔹 Método ARN recibido: {method_arn}")

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
