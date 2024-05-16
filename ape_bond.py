from eth_account import Account
from web3 import Web3
from web3.middleware import geth_poa_middleware

from common import get_private_key, set_max_buy_times, get_max_buy_times, handle_buy_amount
from config import Config
from logger_config import app_logger as logger
import requests
import json


class ApeBondService:
    def __init__(self):
        self.web3 = Web3(provider=Web3.HTTPProvider(Config.HTTP_PROVIDER))
        self.contract_abi = Config.CONTRACT_ABI
        self.chain_id = Config.CHAIN_ID
        self.ape_bonds_api = Config.APE_BONDS_API

    def deposit(self, transaction: dict, bond: dict):
        try:
            logger.info("ApeBondService: deposit called")

            params = transaction.get("contractCall").get("params")
            pid, amount = int(params.get("_pid")), int(params.get("_amount"))
            pid = handle_buy_amount(bond=bond, value=pid)

            # self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
            # contract_address = self.web3.to_checksum_address(transaction.get("to"))
            contract = self.web3.eth.contract(address=transaction.get("to"), abi=self.contract_abi)

            private_key = get_private_key()
            account = Account.from_key(private_key)

            json_txn = {
                'chainId': self.chain_id,
                'gas': transaction.get("gas") + Config.GAS_FEE_ADD,  # 600000
                'gasPrice': self.web3.to_wei(transaction.get("maxFeePerGasGwei") + Config.GAS_FEE_ADD, 'gwei'),
                'nonce': self.web3.eth.get_transaction_count(account.address),
            }

            transaction = contract.functions.deposit(pid, amount, account.address).build_transaction(json_txn)
            logger.info("ApeBondService: transaction before sign")

            # Sign transaction by private key
            signed_transaction = self.web3.eth.account.sign_transaction(transaction, private_key)
            logger.info("ApeBondService: transaction after sign")

            # Send transaction signed to Ethereum
            tx_hash = self.web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

            # Wait for the transaction to be mined
            logger.info("ApeBondService: transaction before mine")
            self.web3.eth.wait_for_transaction_receipt(tx_hash)

            max_buy_times = get_max_buy_times() or []
            max_buy_times.append(dict(bond_contract=bond.get("bond_contract").lower(), quantity=1))
            set_max_buy_times(value=max_buy_times)

            logger.info("ApeBondService: deposit called successfully!")
            return tx_hash.hex()
        except Exception as e:
            logger.warning("ApeBondService: deposit called ERROR")
            raise ValueError(e)

    def get_bond_discount(self):
        try:
            response = requests.get(self.ape_bonds_api)

            if response.status_code != 200:
                logger.warning("ApeBondService: get_ape_bond called Fail")

            jsons = json.loads(response.text)
            bonds = jsons.get(str(Config.CHAIN_ID)).get("bonds")
            bonds_discount = [
                dict(discount=bond.get("discount"), bond_contract=bond.get("billAddress"))
                for bond in bonds if list(filter(
                    lambda x: x.get("bond_contract").lower() == bond.get("billAddress"), Config.BONDS_CONFIG
                ))
            ]

            return bonds_discount
        except Exception as e:
            logger.warning("ApeBondService: get_bond_discount ERROR", exc_info=e)
