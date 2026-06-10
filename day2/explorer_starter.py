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

def decode_transaction(txid):
    """
    TODO:
    1. Call rpc("getrawtransaction", [txid, True])
    2. Print inputs (vin) and outputs (vout)
    """
    tx = rpc("getrawtransaction", [txid, True])

    print(f"Size: {tx['size']} bytes")

    print("\nInputs:")
    for vin in tx['vin']:
        if 'coinbase' in vin:
            print("  COINBASE (mining reward)")
        else:
            print(f"  From: {vin['txid'][:20]}...")

    print("\nOutputs:")
    for vout in tx['vout']:
        addr = vout['scriptPubKey'].get('address', '?')
        value = vout['value']
        print(f"  To: {addr} Amount: {value}")

decode_transaction(txid="e2dcb2d1840817ed3ceda6bb7f7757afec7084c3303691091492ca53724fb4f9")

def show_block(blockhash=None):
    """
    TODO:
    1. if no hash: rpc("getbestblockhash")
    2. Call rpc("getblock", [blockhash, 1])
    3. Print: height, hash, time, tx count
    """
    if blockhash is None:
        blockhash = rpc("getblockhash")

    block = rpc("getblock", [blockhash, 1])

    print(f"=== Block #{block['height']} ===")
    print(f"Hash: {block['hash'][:32]}...")
    print(f"Time: {block['time']}")
    print(f"Transactions: {block['nTx']}")

show_block(blockhash="210190495f87173b60c4a5aea2954acc31ecf0a19e7cd8e55a2b5764f9f5c458")