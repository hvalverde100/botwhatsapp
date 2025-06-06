import os
import requests
from flask import Flask, request
from openai import OpenAI
from prompts import estilo_hub

# Inicializar el cliente de OpenAI usando la API key desde la variable de entorno
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return 'OK', 200

@app.route('/webhook', methods=['POST'])
def webhook():
    # Recibimos form-data de Twilio
    payload = request.form.to_dict()
    print("DEBUG Twilio payload:", payload)

    # Tomamos el mensaje (“Body” o “Cuerpo”) y el remitente
    incoming_msg = payload.get('Body') or payload.get('Cuerpo')
    sender = payload.get('From') or payload.get('De')

    # Llamamos al nuevo endpoint de chat completions
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": estilo_hub},
            {"role": "user",   "content": incoming_msg}
        ]
    )
    texto = response.choices[0].message.content

    # Armamos la respuesta en TwiML para Twilio
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{texto}</Message>
</Response>"""
    return twiml, 200, {'Content-Type': 'application/xml'}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
