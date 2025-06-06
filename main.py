import os
import requests
from flask import Flask, request
from openai import OpenAI
from prompts import estilo_hub

# Inicializar cliente OpenAI
client = OpenAI()

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return 'OK', 200

@app.route('/webhook', methods=['POST'])
def webhook():
    # Twilio manda form-data con la clave 'Body' o 'Cuerpo'
    payload_dict = request.form.to_dict()
    incoming_msg = payload_dict.get('Body') or payload_dict.get('Cuerpo')
    sender = payload_dict.get('From') or payload_dict.get('De')

    # DEBUG: ver lo que llega
    print("DEBUG Twilio payload:", payload_dict)

    # Llamada al nuevo endpoint de chat completions
    chat_resp = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": estilo_hub},
            {"role": "user",   "content": incoming_msg}
        ]
    )
    texto = chat_resp.choices[0].message.content

    # Enviar respuesta en TwiML
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{texto}</Message>
</Response>"""
    return twiml, 200, {'Content-Type': 'application/xml'}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
