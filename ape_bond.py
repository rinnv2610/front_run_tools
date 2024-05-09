import logging

from eth_account import Account
from web3 import Web3
from web3.middleware import geth_poa_middleware

from config import Config

logger = logging.getLogger(__name__)


class ApeBondService:
    def __init__(self):
        self.web3 = Web3(provider=Web3.HTTPProvider(Config.HTTP_PROVIDER))
        self.bond_tracking = Config.SMART_CONTRACT_TRACKING
        self.private_key = Config.PRIVATE_KEY
        self.contract_abi = Config.CONTRACT_ABI
        self.chain_id = Config.CHAIN_ID

    def process_bond(self, input_hash: str) -> (int, int):
        try:
            logger.info("ApeBondService: process_bond called")

            contract = self.web3.eth.contract(abi=self.contract_abi)
            decoded_input = contract.decode_function_input(input_hash)
            decoded_params = decoded_input[1]

            logger.info("ApeBondService: process_bond called successfully!")
            return decoded_params.get("_pid"), decoded_params.get("_amount")
        except Exception as e:
            logger.warning("ApeBondService: process_bond called ERROR with ", exc_info=e)

    def deposit(self, data: dict):
        try:
            logger.info("ApeBondService: deposit called")

            pid, amount = self.process_bond(data.get("input"))

            self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

            contract_address = self.web3.to_checksum_address(self.bond_tracking)
            contract = self.web3.eth.contract(address=contract_address, abi=self.contract_abi)

            account = Account.from_key(self.private_key)
            transaction = contract.functions.deposit(pid, amount, account.address).build_transaction({
                'chainId': self.chain_id,
                'gas': data.get("gas"),  # 600000
                'gasPrice': self.web3.to_wei(data.get("maxFeePerGasGwei") + Config.GAS_FEE_ADD, 'gwei'),
                'nonce': self.web3.eth.get_transaction_count(account.address),
            })

            # Sign transaction by private key
            signed_transaction = self.web3.eth.account.sign_transaction(transaction, self.private_key)

            # Send transaction signed to Ethereum
            tx_hash = self.web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

            # Wait for the transaction to be mined
            # self.web3.eth.wait_for_transaction_receipt(tx_hash)
            logger.info("ApeBondService: deposit called successfully!")
            return tx_hash
        except Exception as e:
            logger.warning("ApeBondService: deposit called ERROR with ", exc_info=e)
