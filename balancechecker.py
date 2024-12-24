import json
from bitcoinlib.wallets import Wallet

def read_private_keys(file_path):
    """Read the private keys from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if not isinstance(data, list):
                raise ValueError(f"Data in {file_path} is not a list.")
            return [item.get('private_key') for item in data if 'private_key' in item]
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error reading JSON in {file_path}: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def save_btc_addresses(file_path, btc_addresses):
    """Save the Bitcoin addresses to a JSON file."""
    try:
        with open(file_path, 'w') as file:
            json.dump({"btc_addresses": btc_addresses}, file, indent=4)
        print(f"Bitcoin addresses saved to {file_path}")
    except Exception as e:
        print(f"Error saving Bitcoin addresses: {e}")

def main():
    private_key_file = 'privatekey.json'
    btc_address_file = 'btcaddress.json'
    
    private_keys = read_private_keys(private_key_file)

    if not private_keys:
        print("No valid private keys found.")
        return

    btc_addresses = []  # List to store generated Bitcoin addresses
    
    # Loop through each private key to generate Bitcoin addresses
    for private_key in private_keys:
        try:
            # Use a unique wallet name based on private key (consider hashing for privacy)
            wallet_name = "TempWallet_" + private_key  
            wallet = Wallet.create(wallet_name, keys=private_key)

            # Get the associated address from the wallet
            if wallet.get_key() is not None:
                btc_address = wallet.get_key().address
                btc_addresses.append(btc_address)  # Append the address to the list

                # Print the generated address
                print(f"Bitcoin Address for private key {private_key}: {btc_address}")

                # Save the BTC address immediately after generation
                save_btc_addresses(btc_address_file, btc_addresses)

            else:
                print(f"No keys found in the wallet: {wallet_name}")

        except Exception as e:
            print(f"Error generating Bitcoin address for private key {private_key}: {e}")

    # Final save of addresses
    if btc_addresses:  # Save if any addresses have been generated
        save_btc_addresses(btc_address_file, btc_addresses)

if __name__ == '__main__':
    main()