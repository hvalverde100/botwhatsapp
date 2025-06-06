import os
import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return 'OK', 200

@app.route('/webhook', methods=['POST'])
def webhook():
    # Twilio envía form data
    payload = request.form.to_dict()
    # Logueo para ver en Render qué llegó
    print("DEBUG payload:", payload)

    # Intento reenviar a Webhook.site
    try:
        r = requests.post(
            "https://webhook.site/e0138e39-fea6-45ff-b655-c8e3d8f9313b",
            json=payload,
            timeout=5
        )
        print("DEBUG forward status:", r.status_code)
    except Exception as e:
        print("ERROR forwarding to webhook.site:", e)

    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
