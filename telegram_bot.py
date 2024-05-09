import logging

import requests

from common import handle_transaction_link
from config import Config

logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self):
        self.bot_token = Config.TELEGRAM_BOT_TOKEN
        self.send_message_to_channel_url = Config.TELEGRAM_BOT_SEND_MESSAGE_CHANNEL_URL
        self.chat_id = Config.CHAT_ID

    def send_message(self, message):
        logger.info("TelegramBot: send_message called")
        url = self.send_message_to_channel_url.format(bot_token=self.bot_token)

        try:
            transaction_link = handle_transaction_link(chain_id=Config.CHAIN_ID, transaction=message)
            message = f'<a href="{transaction_link}">Click to watch transaction</a>'
            response = requests.post(url, json=dict(chat_id=self.chat_id, text=message, parse_mode="HTML"))

            if response.status_code != 200:
                logger.warning("TelegramBot: send_message called fail!")

            logger.info("TelegramBot: send_message called successfully!")
        except Exception as e:
            logger.warning("TelegramBot: send_message called ERROR with ", exc_info=e)
