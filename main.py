import os
import requests
from flask import Flask, request
import openai
from prompts import estilo_hub

# Inicializar app y API key
app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY", "TU_API_KEY_AQUÍ")

# Ruta de health check
@app.route('/health', methods=['GET'])
def health():
    return 'OK', 200

# Endpoint principal de WhatsApp
@app.route('/webhook', methods=['POST'])
def webhook():
    # Capturar datos que manda Twilio
    incoming_msg = request.form.get('Body')
    sender = request.form.get('From')

    # 👉 DEBUG: imprimimos todo el payload que llega
    print("DEBUG Twilio payload:", request.form.to_dict())

    # Lógica de respuesta con ChatGPT
    respuesta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": estilo_hub},
            {"role": "user", "content": incoming_msg}
        ]
    )
    texto = respuesta.choices[0].message["content"]

    # Enviar la respuesta en formato TwiML
    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{texto}</Message>
</Response>"""
    return twiml_response, 200, {'Content-Type': 'application/xml'}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
