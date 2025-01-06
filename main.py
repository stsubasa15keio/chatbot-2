import os
import json
import openai
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

# Flaskアプリの初期化
app = Flask(__name__)

# 環境変数からLINE APIとOpenAI APIのキーを取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# OpenAI APIキーの設定
openai.api_key = OPENAI_API_KEY

@app.route("/callback", methods=["POST"])
def callback():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)

    for event in json_data.get("events", []):
        if event["type"] == "message" and event["message"]["type"] == "text":
            user_message = event["message"]["text"]

            # OpenAI APIで応答生成
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful LINE bot."},
                    {"role": "user", "content": user_message}
                ]
            )
            reply_message = response["choices"][0]["message"]["content"]

            # LINEに応答を送信
            line_bot_api.reply_message(
                event["replyToken"],
                TextSendMessage(text=reply_message)
            )
    return "OK"
