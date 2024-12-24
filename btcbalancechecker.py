import json
import requests

def read_btc_addresses(file_path):
    """Read Bitcoin addresses from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if 'btc_addresses' in data:
                return data['btc_addresses']
            else:
                print("No 'btc_addresses' found in the JSON file.")
                return []
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error reading JSON in {file_path}: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def get_balance_from_tatum(address, api_key):
    """Get the Bitcoin balance for a given address using Tatum API."""
    url = f"https://api.tatum.io/v3/bitcoin/address/balance/{address}"
    headers = {"x-api-key": api_key}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        balance_data = response.json()

        if 'balance' in balance_data:
            return balance_data['balance']
        else:
            print(f"Unexpected response format for address {address}: {balance_data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching balance for {address} from Tatum: {e}")
        return None

def get_balance_from_blockchain_info(address):
    """Get the Bitcoin balance for a given address using Blockchain.info."""
    try:
        r = requests.get(f'https://blockchain.info/q/addressbalance/{address}')
        if r.status_code != 200:
            print('Error fetching balance from Blockchain.info:', r.status_code)
            return None

        balance = int(r.text)
        return balance

    except requests.exceptions.RequestException as e:
        print(f"Error fetching balance for {address} from Blockchain.info: {e}")
        return None

def get_btc_to_usd_conversion_rate():
    """Fetch the current BTC to USD conversion rate from CoinGecko API."""
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
        response.raise_for_status()
        data = response.json()
        return data['bitcoin']['usd']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching BTC to USD conversion rate: {e}")
        return None

def get_block_count(api_key):
    """Fetch the current block count using the Tatum API."""
    url = 'https://bitcoin-mainnet.gateway.tatum.io/'
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'x-api-key': api_key
    }
    body = {
        'jsonrpc': '2.0',
        'method': 'getblockcount',
        'id': 1
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        block_count_data = response.json()
        return block_count_data['result']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching block count: {e}")
        return None

def main():
    # Prompt for address check
    addr = input('Enter address to check (leave empty to skip): ')
    
    if addr:
        balance = get_balance_from_blockchain_info(addr)
        btc_to_usd_rate = get_btc_to_usd_conversion_rate()
        
        if balance is not None and btc_to_usd_rate is not None:
            usd_value = (balance / 100000000) * btc_to_usd_rate  # Convert satoshis to BTC then to USD
            print(f"{addr}\t{balance} sat\t{balance / 100000} mBTC\t{balance / 100000000:.8f} BTC\t${usd_value:.2f}")
        else:
            print(f"Could not retrieve balance for address: {addr}")
        
    # Now check balances for addresses from JSON file
    btc_address_file = 'btcaddress.json'
    api_key = "t-67695bbccefd8d792fbfb96f-15edb620bd4443239c998ea5"  # Replace with your actual Tatum API key

    addresses = read_btc_addresses(btc_address_file)

    if not addresses:
        print("No valid Bitcoin addresses found.")
        return

    for address in addresses:
        balance = get_balance_from_tatum(address, api_key)
        btc_to_usd_rate = get_btc_to_usd_conversion_rate()
        if balance is not None and balance > 0 and btc_to_usd_rate is not None:
            usd_value = balance * btc_to_usd_rate  # Convert balance directly to USD
            print(f"Bitcoin Address: {address} | Balance: {balance} sat | {balance / 100000000:.8f} BTC | ${usd_value:.2f}")
    
    # Fetch and print the current blockchain block count
    block_count = get_block_count(api_key)
    if block_count is not None:
        print(f"Current block count: {block_count}")

if __name__ == '__main__':
    main()