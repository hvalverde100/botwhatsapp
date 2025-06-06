from flask import Flask, request
import openai
from prompts import estilo_hub

app = Flask(__name__)
openai.api_key = "TU_API_KEY"

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.form.get('Body')
    sender = request.form.get('From')

    respuesta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": estilo_hub},
            {"role": "user", "content": incoming_msg}
        ]
    )
    texto = respuesta.choices[0].message["content"]

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{texto}</Message>
</Response>""", 200, {'Content-Type': 'application/xml'}
