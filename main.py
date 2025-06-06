import os
import logging
from flask import Flask, request, Response
from openai import OpenAI
from openai.error import RateLimitError
from prompts import estilo_hub

# Logging
logging.basicConfig(level=logging.INFO)

# Inicializar cliente OpenAI
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    logging.error("❌ OPENAI_API_KEY no encontrada en variables de entorno")
    raise RuntimeError("OPENAI_API_KEY no definida")
client = OpenAI(api_key=api_key)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Superbot activo 👊', 200

@app.route('/health', methods=['GET'])
def health():
    return 'OK', 200

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.form.to_dict()
    logging.info(f"DEBUG Twilio payload: {payload}")

    incoming = payload.get('Body') or payload.get('Cuerpo') or ''
    sender   = payload.get('From') or payload.get('De') or ''

    logging.info(f"Mensaje entrante: '{incoming}' de '{sender}'")
    if not incoming:
        return Response("<Response><Message>No recibí texto 😕</Message></Response>",
                        mimetype='application/xml'), 200

    try:
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": estilo_hub},
                {"role": "user",   "content": incoming}
            ]
        )
        reply = resp.choices[0].message.content.strip()
        logging.info(f"Respuesta OpenAI: {reply}")
    except RateLimitError as e:
        logging.error(f"RateLimitError: {e}")
        reply = "Ups, se acabó el crédito de la API por hoy. Te aviso cuando recargue."
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        reply = "Lo siento, tuve un problema respondiendo. Intenta más tarde."

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>"""
    return Response(xml, mimetype='application/xml'), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    logging.info(f"Arrancando en puerto {port}")
    app.run(host='0.0.0.0', port=port)
