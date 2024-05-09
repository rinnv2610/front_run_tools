import logging

from blocknative.stream import Stream

from ape_bond import ApeBondService
from config import Config
from telegram_bot import TelegramBot

logger = logging.getLogger(__name__)


async def transaction_handler(txn, unsubscribe):
    logger.info("Main: transaction_handler called")

    if txn.get("from") != Config.DEPOSITOR:
        # Output the transaction data to the console
        ape_bond = ApeBondService()
        transaction_hash = ape_bond.deposit(data=txn)

        tele_bot = TelegramBot()
        tele_bot.send_message(transaction_hash)

        logger.info("Main: transaction_handler called successfully!")

        # Unsubscribe from this subscription
        # unsubscribe()


if __name__ == '__main__':
    try:
        logger.info("Main: run bot called")

        stream = Stream(api_key=Config.BLOCK_NATIVE_API_KEY, network_id=int(Config.NETWORK_ID))
        # Register the subscription
        stream.subscribe_address(
            address=Config.SMART_CONTRACT_TRACKING,
            callback=transaction_handler,
            filters=[
                {"status": "pending"},
            ]
        )

        # Start the websocket connection and start receiving events!
        stream.connect()
    except Exception as e:
        logger.error("Main: run bot called ERROR with ", exc_info=e)
