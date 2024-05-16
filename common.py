import random

private_key = None
max_buy_times = []
bonds_discount = []


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


def set_bonds_discount(value):
    global bonds_discount
    bonds_discount = value


def get_bonds_discount():
    return bonds_discount


def handle_transaction_link(chain_id, transaction):
    chain_scan = {
        1: "https://etherscan.io/tx/",
        56: "https://bscscan.com/tx/",
        137: "https://polygonscan.com/tx/",
    }
    return ''.join([chain_scan.get(chain_id), transaction])


def handle_buy_amount(bond, value):
    min_value = int(bond.get("min_value") or 0)
    max_value = int(bond.get("min_value") or 0)

    buy_type_handles = {
        1: value,
        2: min_value * 10**18,
        3: random.randint(min_value, max_value) * 10**18,
    }
    return buy_type_handles.get(bond.get("buy_type"))
