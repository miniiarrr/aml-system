import requests
import json
from datetime import datetime

def get_transaction_details(tx_hash):
    ETHERSCAN_API_KEY = ""
    base_url = "https://api.etherscan.io/api"
    
    # Get internal transactions
    params = {
        "module": "account",
        "action": "txlistinternal",
        "txhash": tx_hash,
        "apikey": ETHERSCAN_API_KEY
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "1" and data["message"] == "OK":
            return data["result"]
        else:
            print(f"Error: {data['message']}")
            return None
    else:
        print(f"Error: HTTP {response.status_code}")
        return None

def get_wallet_transactions(wallet_address, start_block):
    ETHERSCAN_API_KEY = ""
    base_url = "https://api.etherscan.io/api"
    
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': wallet_address,
        'startblock': start_block,
        'endblock': 99999999,
        'sort': 'desc',
        'apikey': ETHERSCAN_API_KEY
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "1" and data["message"] == "OK":
            return data["result"]
        else:
            print(f"Error: {data['message']}")
            return None
    else:
        print(f"Error: HTTP {response.status_code}")
        return None

def get_transaction_method(input_data):
    if not input_data or input_data == "0x":
        return "Transfer"
    # Add more method detection logic here if needed
    return "Contract Interaction"

# Example usage
tx_hash = "0xb61413c495fdad6114a7aa863a00b2e3c28945979a10885b12b30316ea9f072c"
result = get_transaction_details(tx_hash)

transactions = []
if result:
    print("TX_hash")
    print("From")
    print("To")
    print("Amount Currency")
    print("Time")
    print("Method")
    print("---")
    
    for tx in result:
        # Check if amount is greater than 0
        amount = float(tx['value'])/10**18
        if amount <= 0:
            continue
            
        # Convert timestamp to readable format
        timestamp = int(tx['timeStamp'])
        time_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        # Get transaction method
        method = get_transaction_method(tx.get('input', '0x'))
        
        # Create transaction record
        transaction = {
            "tx_hash": tx_hash,
            "parent_tx": None,  # Add parent_tx field as None for initial transactions
            "from": tx['from'],
            "to": tx['to'],
            "amount": amount,
            "currency": "ETH",
            "time": time_str,
            "blockNumber": tx['blockNumber'],
            "method": method,
            "input": tx.get('input', '0x'),
            "depth": 0
        }
        transactions.append(transaction)
        
        # Print formatted output
        print(f"{tx_hash}")
        print(f"{tx['blockNumber']}")
        print(f"{tx['from']}")
        print(f"{tx['to']}")
        print(f"{amount} ETH")
        print(f"{time_str}")
        print(f"{method}")
        print("---")
    
    # Track which transactions have already been processed
    processed_tx_hashes = set(tx['tx_hash'] for tx in transactions)

    # Use a queue to manage breadth-first exploration of transaction layers
    queue = transactions[:]

    while queue:
        current_tx = queue.pop(0)
        dest_wallet = current_tx['to']
        start_block = int(current_tx['blockNumber'])
        parent_tx = current_tx['tx_hash']
        next_depth = current_tx["depth"] + 1

        print(f"\nFetching outgoing transactions for wallet {dest_wallet} starting from block {start_block}")
        print("---")

        wallet_txs = get_wallet_transactions(dest_wallet, start_block)
        if wallet_txs:
            for wallet_tx in wallet_txs:
                if wallet_tx['from'].lower() == dest_wallet.lower():
                    tx_hash = wallet_tx['hash']
                    if tx_hash in processed_tx_hashes:
                        continue

                    amount = float(wallet_tx['value'])/10**18
                    if amount <= 0:
                        continue

                    timestamp = int(wallet_tx['timeStamp'])
                    time_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                    method = get_transaction_method(wallet_tx.get('input', '0x'))

                    wallet_transaction = {
                        "tx_hash": tx_hash,
                        "parent_tx": parent_tx,
                        "from": wallet_tx['from'],
                        "to": wallet_tx['to'],
                        "amount": amount,
                        "currency": "ETH",
                        "time": time_str,
                        "blockNumber": wallet_tx['blockNumber'],
                        "method": method,
                        "input": wallet_tx.get('input', '0x'),
                        "depth": next_depth
                    }

                    transactions.append(wallet_transaction)
                    queue.append(wallet_transaction)
                    processed_tx_hashes.add(tx_hash)

                    # Save updated transactions to file in real-time
                    with open('all_transactions.json', 'w') as f:
                        json.dump(transactions, f, indent=4)

                    print(f"{wallet_tx['hash']}")
                    print(f"{wallet_tx['blockNumber']}")
                    print(f"{wallet_tx['from']}")
                    print(f"{wallet_tx['to']}")
                    print(f"{amount} ETH")
                    print(f"{time_str}")
                    print(f"{method}")
                    print("---")