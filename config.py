import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # TELEGRAM
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    TELEGRAM_BOT_SEND_MESSAGE_CHANNEL_URL = os.environ.get("TELEGRAM_BOT_SEND_MESSAGE_CHANNEL_URL")
    CHAT_ID = os.environ.get("CHAT_ID")

    # BLOCKCHAIN
    PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
    DEPOSITOR = os.environ.get("DEPOSITOR")
    HTTP_PROVIDER = os.environ.get("HTTP_PROVIDER")
    SMART_CONTRACT_TRACKING = os.environ.get("SMART_CONTRACT_TRACKING")
    BLOCK_NATIVE_API_KEY = os.environ.get("BLOCK_NATIVE_API_KEY")
    NETWORK_ID = os.environ.get("NETWORK_ID")
    CHAIN_ID = os.environ.get("CHAIN_ID")
    GAS_FEE_ADD = os.environ.get("GAS_FEE_ADD")
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
            "payable": True,  # Đảm bảo hàm có thể nhận ETH
            "stateMutability": "payable",
            "type": "function"
        }
    ]