import requests, json

def rpc(method, params=None, wallet=None):
    url = "http://127.0.0.1:18443/"
    if wallet:
        url = f"{url}wallet/{wallet}"

    data = json.dumps({
        "jsonrpc": "1.0", "id": "explorer",
        "method": method, "params": params or []
    })

    resp = requests.post(url, data=data, 
        auth=("bootcamp", "bootcamp123"))
    return resp.json()["result"]

def show_blockchain_info():
    """
    TODO:
    1. Call rpc("getblockchaininfo")
    2. Print: chain, blocks, difficulty
    """
    info = rpc("getblockchaininfo")

    print("=== Blockchain Info ===")
    print(f"Chain:      {info['chain']}")
    print(f"Blocks:     {info['blocks']}")
    print(f"Difficulty: {info['difficulty']}")

show_blockchain_info()

def show_wallet_balance(wallet_name):
    """
    TODO:
    1. Load wallet (try/except)
    2. Call rpc("getbalance", [], wallet=wallet_name)
    3. Print the balance
    """
    try:
        rpc("loadwallet", [wallet_name])
    except:
        pass

    balance = rpc("getbalance", [], wallet=wallet_name)

    print(f"=== Wallet: {wallet_name} ===")
    print(f"Balance: {balance} BTC")

show_wallet_balance(wallet_name="alice")

def list_transactions(wallet_name, count=5):
    """
    TODO:
    1. Call rpc("listtransactions", ["*", count], wallet=wallet_name)
    2. For each tx: print direction, amount, txid
    """
    try:
        rpc("loadwallet", [wallet_name])
    except:
        pass

    txs = rpc("listtransactions", ["*", count], wallet=wallet_name)

    for tx in txs:
        if tx['category'] in ('receive', 'generate', 'immature'):
            direction = "IN"
        else:
            direction = "OUT"

        print(f"{direction} {tx['amount']:+.8f} BTC")

list_transactions(wallet_name="alice")