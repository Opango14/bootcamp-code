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

info = rpc("getblockchaininfo")
print(f"Chain: {info['chain']}")
print(f"Blocks: {info['blocks']}")

balance = rpc("getbalance", [], wallet="bob")
print(f"Bob has {balance} BTC")