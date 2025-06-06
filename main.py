@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.form.to_dict()
    print("DEBUG Twilio payload:", payload)

    incoming_msg = payload.get('Body') or payload.get('Cuerpo')
    if not incoming_msg:
        return "", 204

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": estilo_hub},
                {"role": "user", "content": incoming_msg}
            ]
        )
        texto = response.choices[0].message.content.strip()
    except Exception as e:
        print("Error OpenAI:", e)
        texto = "Lo siento, tuve un problema respondiendo tu mensaje."

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{texto}</Message>
</Response>"""
    return twiml, 200, {'Content-Type': 'application/xml'}
