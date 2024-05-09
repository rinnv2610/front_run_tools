import argparse
import logging

from blocknative.stream import Stream

from ape_bond import ApeBondService
from common import set_private_key
from config import Config
from telegram_bot import TelegramBot

logger = logging.getLogger(__name__)


async def transaction_handler(transaction, unsubscribe):
    logger.info("Main: transaction_handler called")

    if transaction.get("from") == Config.DEPOSITOR:
        return

    # Output the transaction data to the console
    logger.info(f"Main: transaction_handler called with {transaction}")
    ape_bond = ApeBondService()
    transaction_hash = ape_bond.deposit(data=transaction)

    # logger.info(f"Main: transaction_handler called with transaction_hash {transaction_hash}")
    tele_bot = TelegramBot()
    tele_bot.send_message(transaction_hash)

    logger.info("Main: transaction_handler called successfully!")

    # Unsubscribe from this subscription
    # unsubscribe()


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--private_key", type=str, required=True)
    #
    # args = parser.parse_args()
    # set_private_key(value=args.private_key)

    try:
        logger.info("Main: run bot called")

        stream = Stream(api_key=Config.BLOCK_NATIVE_API_KEY, network_id=Config.NETWORK_ID)
        # Register the subscription
        stream.subscribe_address(
            address=Config.SMART_CONTRACT_TRACKING,
            callback=transaction_handler,
            filters=[
                {"status": "pending"},
            ],
            abi=Config.CONTRACT_ABI
        )

        # Start the websocket connection and start receiving events!
        stream.connect()
    except Exception as e:
        logger.error("Main: run bot called ERROR with ", exc_info=e)
