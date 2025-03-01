import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

WEBHOOK_VERIFY_TOKEN = os.getenv("1234")
GRAPH_API_TOKEN = os.getenv("EAAg9azoNUlcBOxi7ljbuZC5p2a0iTjhnbva82XOyKsC3sCpdnGkzPSz6rwDhziwZCahewfJulpI6GV08ZCugyuZByDmyez5Wn9pDFfhkJJJiY0u2jB2PIWse8hFiUG3QpcsKBG0zTqlo65EZCx80OZAMZC9M0by9W3355uZCMdexaCgc7ZBT5l9KMNZBb5IKdOipe1WLI3cqdOUW1Sa4ZBZAoRsZACLtEu7IU")
PORT = int(os.getenv("PORT", 5000))

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Incoming webhook message:", json.dumps(data, indent=2))

    # Extraer el mensaje entrante
    message = data.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}).get("messages", [{}])[0]

    # Verificar si el mensaje es de tipo texto
    if message.get("type") == "text":
        business_phone_number_id = data["entry"][0]["changes"][0]["value"]["metadata"]["phone_number_id"]

        # Enviar respuesta a través de la API de WhatsApp
        response = requests.post(
            f"https://graph.facebook.com/v18.0/{business_phone_number_id}/messages",
            headers={"Authorization": f"Bearer {GRAPH_API_TOKEN}"},
            json={
                "messaging_product": "whatsapp",
                "to": message["from"],
                "text": {"body": "Mensaje recibido, gracias!"}
            }
        )

        print("Response from WhatsApp API:", response.json())

    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
