import os
import logging
from flask import Flask, request
from openai import OpenAI
from prompts import estilo_hub

# Configurar logging para debug
logging.basicConfig(level=logging.INFO)

# Inicializar cliente OpenAI
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    logging.error("No se encontró la variable OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return 'OK', 200

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.form.to_dict()
    logging.info(f"DEBUG Carga útil de Twilio: {payload}")

    incoming_msg = payload.get('Body') or payload.get('Cuerpo') or ''
    sender = payload.get('From') or payload.get('De') or ''

    logging.info(f"incoming_msg: '{incoming_msg}' sender: '{sender}'")

    if not incoming_msg:
        logging.warning("No se recibió mensaje en el payload")
        return "", 400  # Bad Request

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": estilo_hub},
                {"role": "user", "content": incoming_msg}
            ]
        )
        texto = response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error llamando a OpenAI: {e}")
        texto = "Lo siento, ahora mismo no puedo responder. Intenta más tarde."

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{texto}</Message>
</Response>"""
    return twiml, 200, {'Content-Type': 'application/xml'}


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
