# 必要なライブラリのインポート
import os
from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import logging  # ロギングを追加

# 環境変数の読み込み
load_dotenv()
CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# ログの設定
logging.basicConfig(level=logging.DEBUG)

# Flaskアプリケーションの初期化
app = Flask(__name__)
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# OpenAI APIキーの設定
openai.api_key = OPENAI_API_KEY

# Webhookエンドポイントの設定
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        logging.error(f"Error in webhook: {e}")
        abort(400)

    return 'OK'

# LINEメッセージイベントの処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text  # ユーザーからのメッセージ

    try:
        # OpenAI APIを呼び出して応答を取得
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        reply_message = response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        # OpenAI API関連のエラーが発生した場合
        logging.error(f"OpenAI API error: {e}")
        reply_message = "OpenAI APIに問題が発生しました。後ほどお試しください。"
    except Exception as e:
        # その他のエラーが発生した場合
        logging.error(f"Unexpected error: {e}")
        reply_message = "エラーが発生しました。もう一度お試しください。"

    # LINEユーザーに応答を送信
    try:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
    except Exception as e:
        logging.error(f"Error in replying to LINE user: {e}")

# アプリケーションの起動
if __name__ == "__main__":
    app.run(debug=True)
