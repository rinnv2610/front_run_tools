import argparse
from blocknative.stream import Stream

from ape_bond import ApeBondService
from common import set_private_key
from config import Config
from telegram_bot import TelegramBot
from concurrent.futures import ThreadPoolExecutor
from logger_config import app_logger as logger


async def transaction_handler(transaction, unsubscribe):
    logger.info(f"Main: transaction_handler called with {transaction}")

    if transaction.get("from") in Config.BLACK_USERS:
        logger.info("Main: transaction_handler called with transaction of black users")
        return

    # Output the transaction data to the console
    ape_bond = ApeBondService()
    transaction_hash = ape_bond.deposit(data=transaction)

    # logger.info(f"Main: transaction_handler called with transaction_hash {transaction_hash}")
    tele_bot = TelegramBot()
    tele_bot.send_message(transaction_hash)

    logger.info("Main: transaction_handler called successfully!")

    # Unsubscribe from this subscription
    unsubscribe()


def do_process(bond: dict):
    try:
        logger.info("Main: do_process called")
        # Register the subscription
        stream = Stream(api_key=Config.BLOCK_NATIVE_API_KEY, network_id=Config.NETWORK_ID)
        stream.subscribe_address(
            address=bond.get("bond_contract"),
            callback=transaction_handler,
            filters=[
                {"status": "pending"},
            ],
            abi=Config.CONTRACT_ABI
        )

        # Start the websocket connection and start receiving events!
        stream.connect()
    except Exception as e:
        logger.error("Main: do_process called ERROR with ", exc_info=e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--private_key", type=str, required=False, default=Config.PRIVATE_KEY)

    args = parser.parse_args()
    set_private_key(value=args.private_key)

    logger.info("Main: run bot start")
    bonds_config = Config.BONDS_CONFIG

    with ThreadPoolExecutor(max_workers=len(bonds_config)) as executor:
        # Submit tasks to the executor
        futures = [executor.submit(do_process, bond) for bond in bonds_config]

    logger.info("Main: run bot end")
