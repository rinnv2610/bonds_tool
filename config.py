import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    APE_BONDS_URL = os.environ.get('APE_BONDS_URL')
    TELEGRAM_BOT_SEND_MESSAGE_CHANNEL_URL = os.environ.get('TELEGRAM_BOT_SEND_MESSAGE_CHANNEL_URL')
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    CHAINS = os.environ.get('CHAINS')
    CHAT_ID = os.environ.get('CHAT_ID')
