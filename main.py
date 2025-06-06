from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import os, openai
from openai.error import RateLimitError

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    resp = MessagingResponse()

    if not incoming_msg:
        resp.message("¿Me escribiste algo? No lo veo.")
        return str(resp)

    try:
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un bot amigable de Mercado Mayoreo."},
                {"role": "user",   "content": incoming_msg}
            ]
        )
        reply = chat.choices[0].message.content.strip()
    except RateLimitError:
        reply = "Se acabó el crédito de la API por hoy. Te aviso cuando recargue."
    except Exception as e:
        print("Error inesperado:", e)
        reply = "Lo siento, hubo un problema. Intenta más tarde."

    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
