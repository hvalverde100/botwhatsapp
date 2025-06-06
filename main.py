import os
import logging
from flask import Flask, request
from openai import OpenAI
from openai.error import RateLimitError
from prompts import estilo_hub

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Inicializar cliente OpenAI con API Key
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return 'OK', 200

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.form.to_dict()
    logging.info(f"DEBUG Twilio payload: {payload}")

    incoming_msg = payload.get('Body') or payload.get('Cuerpo')
    sender = payload.get('From') or payload.get('De')

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": estilo_hub},
                {"role": "user", "content": incoming_msg}
            ]
        )
        texto = response.choices[0].message.content
        logging.info(f"Respuesta para {sender}: {texto}")

    except RateLimitError as e:
        texto = ("Oops, se acabó el crédito de la API. "
                 "Por favor avísame para recargar y seguir conversando.")
        logging.error(f"RateLimitError: {e} - Usuario: {sender}")
        # Aquí podés poner cualquier notificación extra, ejemplo:
        # send_email("Alerta API OpenAI", f"Rate limit superado por {sender}")
        # o mandar mensaje a Telegram, Slack, etc.
        print(f"[ALERTA] Límite de API excedido. Usuario: {sender}")

    except Exception as e:
        texto = "Lo siento, hubo un error procesando tu mensaje. Intenta de nuevo."
        logging.error(f"Error inesperado: {e} - Usuario: {sender}")
        print(f"[ERROR] Excepción no controlada: {e}")

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{texto}</Message>
</Response>"""
    return twiml, 200, {'Content-Type': 'application/xml'}


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    logging.info(f"Arrancando servidor en puerto {port}")
    app.run(host='0.0.0.0', port=port)
