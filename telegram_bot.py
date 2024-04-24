import requests

from config import Config


class TelegramBot:
    def __init__(self):
        self.bot_token = Config.TELEGRAM_BOT_TOKEN
        self.send_message_to_channel_url = Config.TELEGRAM_BOT_SEND_MESSAGE_CHANNEL_URL
        self.chat_id = Config.CHAT_ID

    def send_message(self, message):
        url = self.send_message_to_channel_url.format(bot_token=self.bot_token)

        try:
            response = requests.post(url, json=dict(chat_id=self.chat_id, text=message, parse_mode="HTML"))

            if response.status_code == 200:
                print('Message sent successfully!')
            else:
                print('Failed to send message:', response.text)

        except Exception as e:
            print(e)
