from flask import Flask, request
import requests
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Twilio manda form data, no JSON
    payload = request.form.to_dict()

    # Re-envío a Webhook.site para chequear que llegue
    requests.post(
        "https://webhook.site/e0138e39-fea6-45ff-b655-c8e3d8f9313b",
        json=payload
    )
    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
