from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
import openai
from constant import CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET, OPENAI_API_KEY

# Flaskアプリの初期化
app = Flask(__name__)

# LINE APIとOpenAI APIの設定
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
openai.api_key = OPENAI_API_KEY

@app.route("/callback", methods=["POST"])
def callback():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)

    for event in json_data.get("events", []):
        if event["type"] == "message" and event["message"]["type"] == "text":
            user_message = event["message"]["text"]

            # OpenAI APIで応答を生成
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
