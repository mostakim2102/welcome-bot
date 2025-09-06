from flask import Flask, request
import requests
import os
import random

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# Welcome message templates
templates = [
    "স্বাগতম {name}! 🎉",
    "হাই {name}, গ্রুপে যোগ হওয়ায় ধন্যবাদ! 😃",
    "Hello {name}! আশা করি মজা করবেন। 🎈"
]

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    # নতুন ইউজার যোগ হলে
    if "message" in data and "new_chat_members" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        new_users = data["message"]["new_chat_members"]
        for user in new_users:
            first_name = user.get("first_name", "User")
            username = user.get("username")
            message_template = random.choice(templates)
            welcome_text = message_template.format(name=first_name)
            if username:
                welcome_text += f" (@{username})"
            requests.post(TELEGRAM_API, json={"chat_id": chat_id, "text": welcome_text})

    # কমান্ড হ্যান্ডলিং
    elif "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"].lower()

        if text == "/start":
            reply = "হাই! আমি স্বাগতম বট। আমি নতুন মেম্বারদের স্বাগত জানাই।"
            requests.post(TELEGRAM_API, json={"chat_id": chat_id, "text": reply})

        elif text == "/help":
            reply = "আমি স্বাগতম বট। গ্রুপে কেউ যোগ হলে স্বয়ংক্রিয়ভাবে মেসেজ পাঠাই।"
            requests.post(TELEGRAM_API, json={"chat_id": chat_id, "text": reply})

    return "ok"
