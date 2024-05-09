private_key = None


def set_private_key(value):
    global private_key
    private_key = value


def get_private_key():
    return private_key


def handle_transaction_link(chain_id, transaction):
    chain_scan = {
        1: "https://etherscan.io/tx/",
        56: "https://bscscan.com/tx/",
        137: "https://polygonscan.com/tx/",
    }
    return ''.join([chain_scan.get(chain_id), transaction])
