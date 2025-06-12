from flask import Flask, request
import requests
import os
from openai import OpenAI

app = Flask(__name__)

# Lấy token từ biến môi trường
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

client = OpenAI(api_key=OPENAI_API_KEY)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"]["text"]

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Bạn là một trợ lý thông minh, thân thiện, trả lời tự nhiên bằng tiếng Việt."},
                    {"role": "user", "content": user_text}
                ]
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"Đã xảy ra lỗi khi trả lời: {str(e)}"

        # Gửi phản hồi về Telegram
        requests.post(TELEGRAM_URL, json={"chat_id": chat_id, "text": reply})
    return "OK"

@app.route("/", methods=["GET"])
def index():
    return "GPT bot (OpenAI v1.x) is running"

if __name__ == "__main__":
    app.run()