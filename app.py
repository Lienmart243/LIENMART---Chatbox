from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Cho phép CORS để giao tiếp với client (HTML)

openai.api_key = "sk-..."  # Thay bằng API key ChatGPT của bạn

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        message = data.get("message", "")
        if not message:
            return jsonify({"error": "Missing message"}), 400

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )

        reply = response["choices"][0]["message"]["content"]
        return jsonify({"content": reply.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)