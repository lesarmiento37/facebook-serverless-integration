import json
import os

def lambda_handler(event, context):
    """Manejo de eventos HTTP de API Gateway para la integración con Facebook Messenger."""
    print("📥 Evento recibido:", json.dumps(event, indent=2))

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
    """Verifica el webhook de Facebook mediante el método GET, esperando Authorization en los headers."""
    try:
        headers = event.get("headers", {})

        # Obtener el Authorization token del header
        received_token = headers.get("Authorization", "")
        expected_token = os.getenv("FACEBOOK_VERIFY_TOKEN", "")

        if received_token == expected_token:
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Verificación exitosa"})
            }
        else:
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
        print("📩 Evento recibido de Facebook:", json.dumps(body, indent=2))

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