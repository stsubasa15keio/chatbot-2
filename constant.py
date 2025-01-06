import os
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

# LINE Botの設定
CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')

# OpenAI APIの設定
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
