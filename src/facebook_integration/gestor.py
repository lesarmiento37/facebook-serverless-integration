import json
import os
import boto3
from datetime import datetime
import uuid

# Configurar el cliente de DynamoDB
dynamodb = boto3.resource("dynamodb")
table_name = os.getenv("DYNAMODB_TABLE", "table_test")
table = dynamodb.Table(table_name)


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
def insert_into_dynamodb(mensaje):
    """Procesa eventos con formato personalizado y los inserta en DynamoDB."""
    try:
        message_id = str(uuid.uuid4())  # Generar un UUID único
        text = mensaje.get("Text", "No text provided").strip()
        sentiment = mensaje.get("Sentiment", "Unknown").strip()
        timestamp_str = mensaje.get("Timestamp", "")
        timestamp = int(datetime.strptime(timestamp_str, "%d/%m/%Y %H:%M").timestamp()) if timestamp_str else int(datetime.utcnow().timestamp())
        user = mensaje.get("User", "Unknown User").strip()
        platform = mensaje.get("Platform", "Unknown Platform").strip()
        hashtags = mensaje.get("Hashtags", "").strip()
        retweets = int(mensaje.get("Retweets", 0))
        likes = int(mensaje.get("Likes", 0))
        country = mensaje.get("Country", "Unknown Country").strip()
        year = int(mensaje.get("Year", 0))
        month = int(mensaje.get("Month", 0))
        day = int(mensaje.get("Day", 0))
        hour = int(mensaje.get("Hour", 0))

        # Insertar en DynamoDB
        table.put_item(
            Item={
                "message_id": message_id,
                "text": text,
                "sentiment": sentiment,
                "timestamp": timestamp,
                "user": user,
                "platform": platform,
                "hashtags": hashtags,
                "retweets": retweets,
                "likes": likes,
                "country": country,
                "year": year,
                "month": month,
                "day": day,
                "hour": hour
            }
        )
        print(f"✅ Mensaje {message_id} guardado en DynamoDB")

        return {
            "statusCode": 200,
            "body": json.dumps({"status": "received", "message_id": message_id})
        }

    except Exception as e:
        print(f"❌ Error al guardar en DynamoDB: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error interno al guardar en la base de datos"})
        }