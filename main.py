from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import os
import openai
from openai.error import RateLimitError

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        incoming_msg = request.values.get("Body", "").strip()
        print("DEBUG Twilio payload:", request.values)

        if not incoming_msg:
            resp = MessagingResponse()
            resp.message("No recibí ningún mensaje, ¿puedes intentar de nuevo?")
            return str(resp)

        # Llamada a OpenAI ChatCompletion
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente amigable y útil."},
                {"role": "user", "content": incoming_msg}
            ],
            max_tokens=500,
            temperature=0.7,
        )

        reply_text = response.choices[0].message.content.strip()

    except RateLimitError:
        # Manejo cuando se excede la cuota de OpenAI
        print("ERROR: Se excedió la cuota de la API de OpenAI")
        reply_text = "Ups, he llegado al límite de uso hoy. Intenta más tarde."

    except Exception as e:
        print("ERROR inesperado:", e)
        reply_text = "Lo siento, hubo un problema al procesar tu mensaje."

    resp = MessagingResponse()
    resp.message(reply_text)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=10000)
