import json
import requests
import boto3
import os

################ Main handler #########################
def lambda_handler(event, context):
    """Manejo de eventos HTTP de API Gateway para la integración con Facebook Messenger."""
    
    http_method = event.get("httpMethod", "")
    path = event.get("path", "")

    if http_method == "GET":
        return handle_verification(event)
    elif http_method == "POST":
        return handle_webhook(event)

    return {
        "statusCode": 400,
        "body": json.dumps({"message": "Método no permitido"})
    }


def handle_verification(event):
    """Verifica el webhook de Facebook con GET"""
    query_params = event.get("queryStringParameters", {})

    mode = query_params.get("hub.mode")
    token = query_params.get("hub.verify_token")
    challenge = query_params.get("hub.challenge")

    VERIFY_TOKEN = os.getenv("FACEBOOK_VERIFY_TOKEN")  # Token de verificación en variables de entorno

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return {
            "statusCode": 200,
            "body": challenge
        }
    else:
        return {
            "statusCode": 403,
            "body": json.dumps({"message": "Verificación fallida"})
        }


def handle_webhook(event):
    """Recibe eventos de Facebook con POST y los imprime"""
    body = json.loads(event.get("body", "{}"))

    print("📩 Evento recibido:", body)

    return {
        "statusCode": 200,
        "body": json.dumps({"status": "received"})
    }
