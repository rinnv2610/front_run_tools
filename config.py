import json
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # TELEGRAM
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    TELEGRAM_BOT_SEND_MESSAGE_CHANNEL_URL = os.environ.get("TELEGRAM_BOT_SEND_MESSAGE_CHANNEL_URL")
    CHAT_ID = int(os.environ.get("CHAT_ID"))

    # BLOCKCHAIN
    PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
    HTTP_PROVIDER = os.environ.get("HTTP_PROVIDER")
    BLOCK_NATIVE_API_KEY = os.environ.get("BLOCK_NATIVE_API_KEY")
    NETWORK_ID = int(os.environ.get("NETWORK_ID"))
    CHAIN_ID = int(os.environ.get("CHAIN_ID"))
    GAS_FEE_ADD = int(os.environ.get("GAS_FEE_ADD"))
    BLACK_USERS = json.loads(os.environ.get("BLACK_USERS"))
    BONDS_CONFIG = json.loads(os.environ.get("BONDS_CONFIG"))
    APE_BONDS_API = os.environ.get("APE_BONDS_API")
    CONTRACT_ABI = [
        {
            "constant": False,
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "_pid",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "_amount",
                    "type": "uint256"
                },
                {
                    "internalType": "address",
                    "name": "_referrer",
                    "type": "address"
                },
            ],
            "name": "deposit",
            "outputs": [],
            "payable": True,
            "stateMutability": "payable",
            "type": "function"
        }
    ]
