from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    # চেক করি কোন নতুন ইউজার যোগ হয়েছে কি না
    if "message" in data and "new_chat_members" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        new_users = data["message"]["new_chat_members"]
        for user in new_users:
            username = user.get("first_name", "User")
            welcome_text = f"স্বাগতম {username}! গ্রুপে যোগ হওয়ায় ধন্যবাদ। 🎉"
            requests.post(TELEGRAM_API, json={"chat_id": chat_id, "text": welcome_text})

    return "ok"
