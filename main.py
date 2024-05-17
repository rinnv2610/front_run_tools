import argparse
import time

import schedule
from blocknative.stream import Stream

from ape_bond import ApeBondService
from common import set_private_key, set_bonds_discount, get_bonds_discount, get_max_buy_times
from config import Config
from telegram_bot import TelegramBot
from concurrent.futures import ThreadPoolExecutor
from logger_config import app_logger as logger

ape_bond = ApeBondService()


async def handler_transaction(transaction, unsubscribe):
    logger.info(f"Main: transaction_handler called with {transaction}")

    if transaction.get("from") in Config.BLACK_USERS:
        logger.info("Main: transaction is black users")
        return

    bond = list(filter(lambda x: x.get("bond_contract") == transaction.get("to"), Config.BONDS_CONFIG))[0]
    bond_contract = bond.get("bond_contract").lower()
    bonds_discount = get_bonds_discount()
    if list(filter(
            lambda x: x.get("bond_contract") == bond_contract and
                      (x.get("discount") <= 0 or x.get("discount") < bond.get("min_discount")), bonds_discount)):
        logger.info("Main: bond discount invalid")
        return

    max_buy_times = get_max_buy_times()
    if max_buy_times and list(
            filter(lambda x: x.get("bond_contract") == bond_contract and x.get("quantity", 0) == 1, max_buy_times)):
        logger.info("Main: max buy times to limit")
        return

    transaction_hash = ape_bond.deposit(transaction=transaction, bond=bond)

    # logger.info(f"Main: transaction_handler called with transaction_hash {transaction_hash}")
    tele_bot = TelegramBot()
    tele_bot.send_message(transaction_hash)

    logger.info("Main: transaction_handler called successfully!")

    # Unsubscribe from this subscription
    # unsubscribe()


def do_process(bond: dict):
    try:
        logger.info(f'Main: do_process called with contract {bond.get("bond_contract")}')
        # Register the subscription
        stream = Stream(api_key=Config.BLOCK_NATIVE_API_KEY, network_id=Config.NETWORK_ID)
        stream.subscribe_address(
            address=bond.get("bond_contract"),
            callback=handler_transaction,
            filters=[
                {"status": "pending"},
            ],
            abi=Config.CONTRACT_ABI
        )

        # Start the websocket connection and start receiving events!
        stream.connect()
    except Exception as e:
        logger.error("Main: do_process called ERROR with ", exc_info=e)


def save_bond_discount_to_global():
    logger.info("Main: save_bond_discount_to_global called")
    set_bonds_discount(value=ape_bond.get_bond_discount())
    logger.info("Main: save_bond_discount_to_global called successfully!")


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule.every(10).minutes.do(save_bond_discount_to_global)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--private_key", type=str, required=True)

    args = parser.parse_args()
    set_private_key(value=args.private_key)

    logger.info("Main: run bot start")

    # Set discount bond contract to global variable
    set_bonds_discount(value=ape_bond.get_bond_discount())

    with ThreadPoolExecutor(max_workers=len(Config.BONDS_CONFIG)) as executor:
        # Submit tasks to the executor
        futures = [executor.submit(do_process, bond) for bond in Config.BONDS_CONFIG]
        run_scheduler()

    logger.info("Main: run bot end")
