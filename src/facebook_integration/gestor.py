import json
import os

def lambda_handler(event, context):
    """Manejo de eventos HTTP de API Gateway para la integración con Facebook Messenger."""
    print("📥 Evento recibido:", json.dumps(event, separators=(',', ':')))

    http_method = event.get("httpMethod", "")

    if http_method == "GET":
        return handle_verification(event)
    elif http_method == "POST":
        return handle_webhook(event)

    return {
        "statusCode": 405,
        "body": json.dumps({"message": "Método no permitido"})
    }

def handle_verification(event):
    """Verifica el webhook de Facebook mediante el método GET."""
    try:
        query_params = event.get("queryStringParameters", {})

        mode = query_params.get("hub.mode", "")
        token = query_params.get("hub.verify_token", "")
        challenge = query_params.get("hub.challenge", "")

        expected_token = os.getenv("FACEBOOK_VERIFY_TOKEN", "xyz987")

        if mode == "subscribe" and token == expected_token:
            print("✅ Facebook verification exitosa")
            return {
                "statusCode": 200,
                "body": challenge
            }
        else:
            print("🚫 Verificación fallida")
            return {
                "statusCode": 403,
                "body": json.dumps({"message": "Verificación fallida"})
            }

    except Exception as e:
        print("❌ Error en la verificación:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error interno del servidor"})
        }

def handle_webhook(event):
    """Recibe eventos de Facebook mediante POST y los procesa."""
    try:
        body = json.loads(event.get("body", "{}"))
        print("📩 Evento recibido de Facebook:", json.dumps(body, separators=(',', ':')))


        return {
            "statusCode": 200,
            "body": json.dumps({"status": "received"})
        }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Error en el formato JSON"})
        }
    except Exception as e:
        print("❌ Error al procesar el webhook:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error interno del servidor"})
        }
