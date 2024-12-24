import json
import os
import requests
from bitcoinlib.wallets import Wallet

def generate_private_key():
    """Generate a random Bitcoin private key."""
    return os.urandom(32).hex()  # Generate a random 32 bytes and convert to hexadecimal

def private_key_to_public_address(private_key):
    """Convert a private key to a Bitcoin public address."""
    # Create a Wallet (in-memory)
    w = Wallet.create('MyWallet')
    
    # Add a key (this derives the public address)
    key = w.get_key(private_key)
    
    return key.address, key.private_hex

def save_private_key_to_file(private_key, filename):
    """Saves the private key in JSON format to the specified filename."""
    with open(filename, 'w') as f:
        json.dump({"private_key": private_key}, f)
    print(f"Private key saved to {filename}")

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
    # Generate a private key
    private_key = generate_private_key()
    print(f"Generated Private Key: {private_key}")

    # Save the private key to a JSON file immediately
    save_private_key_to_file(private_key, 'privatekey.json')

    # Get the public address from the private key
    public_address, derived_private_key = private_key_to_public_address(private_key)
    print(f"Derived Public Address: {public_address}")

    # Fetch and print the current blockchain block count
    api_key = 't-67695bbccefd8d792fbfb96f-15edb620bd4443239c998ea5'  # Replace with your actual Tatum API key
    block_count = get_block_count(api_key)
    
    if block_count is not None:
        print(f"Current block count: {block_count}")

if __name__ == '__main__':
    main()