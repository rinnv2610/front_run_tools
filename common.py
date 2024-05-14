from enum import Enum

private_key = None
max_buy_times = None


def set_private_key(value):
    global private_key
    private_key = value


def get_private_key():
    return private_key


def set_max_buy_times(value):
    global max_buy_times
    max_buy_times = value


def get_max_buy_times():
    return max_buy_times


def handle_transaction_link(chain_id, transaction):
    chain_scan = {
        1: "https://etherscan.io/tx/",
        56: "https://bscscan.com/tx/",
        137: "https://polygonscan.com/tx/",
    }
    return ''.join([chain_scan.get(chain_id), transaction])


class BuyTypeEnum(Enum):
    BOND_EQUAL = 1
    MIN_EQUAL = 2
    RANDOM = 3
    BUY = 4
