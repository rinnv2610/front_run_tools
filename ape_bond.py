from eth_account import Account
from web3 import Web3
from web3.middleware import geth_poa_middleware

from common import get_private_key
from config import Config
from logger_config import app_logger as logger


class ApeBondService:
    def __init__(self):
        self.web3 = Web3(provider=Web3.HTTPProvider(Config.HTTP_PROVIDER))
        self.bond_tracking = Config.SMART_CONTRACT_TRACKING
        self.private_key = get_private_key()
        self.contract_abi = Config.CONTRACT_ABI
        self.chain_id = Config.CHAIN_ID

    def deposit(self, data: dict):
        try:
            logger.info("ApeBondService: deposit called")

            params = data.get("contractCall").get("params")
            pid, amount = int(params.get("_pid")), int(params.get("_amount"))

            # self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
            # contract_address = self.web3.to_checksum_address(self.bond_tracking)
            contract = self.web3.eth.contract(address=self.bond_tracking, abi=self.contract_abi)

            account = Account.from_key(self.private_key)
            json_txn = {
                'chainId': self.chain_id,
                'gas': data.get("gas"),  # 600000
                'gasPrice': self.web3.to_wei(data.get("maxFeePerGasGwei") + Config.GAS_FEE_ADD, 'gwei'),
                'nonce': self.web3.eth.get_transaction_count(account.address),
            }

            transaction = contract.functions.deposit(pid, amount, account.address).build_transaction(json_txn)
            logger.info("ApeBondService: transaction before sign")

            # Sign transaction by private key
            signed_transaction = self.web3.eth.account.sign_transaction(transaction, self.private_key)
            logger.info("ApeBondService: transaction after sign")

            # Send transaction signed to Ethereum
            tx_hash = self.web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

            # Wait for the transaction to be mined
            logger.info("ApeBondService: transaction before mine")
            self.web3.eth.wait_for_transaction_receipt(tx_hash)

            logger.info("ApeBondService: deposit called successfully!")
            return tx_hash.hex()
        except Exception as e:
            logger.warning("ApeBondService: deposit called ERROR")
            raise ValueError(e)
