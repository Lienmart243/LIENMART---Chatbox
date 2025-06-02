from flask import Flask, request, jsonify
import openai
import os
import traceback
from dotenv import load_dotenv

# Load biến môi trường từ file .env (nếu chạy local)
load_dotenv()

# Lấy API Key từ biến môi trường
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    print("❌ Không tìm thấy biến môi trường OPENAI_API_KEY")

# Khởi tạo Flask app
app = Flask(__name__)

# Route chính cho chat
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message")

    if not message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là một trợ lý ảo thông minh của LIENMART. Hãy trả lời bằng tiếng Việt."},
                {"role": "user", "content": message}
            ]
        )
        reply = response.choices[0].message["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        print("❌ Lỗi khi gọi OpenAI:", e)
        traceback.print_exc()
        return jsonify({"error": "Có lỗi xảy ra từ hệ thống"}), 500

# Route kiểm tra trạng thái server
@app.route("/", methods=["GET"])
def index():
    return "✅ LIENMART Chatbox is running."

# Chạy app local (Render sẽ bỏ qua phần này)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
