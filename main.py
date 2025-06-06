import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Clave y endpoint de OpenRouter (gratuito)
openai.api_key = "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"
openai.api_base = "https://openrouter.ai/api/v1"

@app.route("/", methods=["GET"])
def home():
    return "¡Hola desde tu superbot en Render! 😎"

@app.route("/bot", methods=["POST"])
def bot():
    user_message = request.json.get("message", "")
    
    response = openai.ChatCompletion.create(
        model="mistralai/mixtral-8x7b",
        messages=[
            {"role": "system", "content": "Sos un asistente simpático, directo, como un buen amigo tico."},
            {"role": "user", "content": user_message}
        ]
    )

    return jsonify({
        "response": response["choices"][0]["message"]["content"]
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)


