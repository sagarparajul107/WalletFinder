import secrets
import ecdsa
import hashlib
import time
import json
from datetime import datetime
from colorama import Fore, Style, init
import threading

# Initialize colorama
init()

def generate_private_key():
    """Generates a random 32-byte private key."""
    return secrets.token_bytes(32)  # Return as raw bytes

def generate_public_key(private_key_bytes):
    """Generates a public key from a given private key in raw byte format."""
    private_key_int = int.from_bytes(private_key_bytes, 'big')
    sk = ecdsa.SigningKey.from_secret_exponent(private_key_int, curve=ecdsa.SECP256k1)
    public_key = sk.verifying_key.to_string()  # Public key as bytes
    return public_key

def get_current_timestamp():
    """Returns the current timestamp in ISO format."""
    return datetime.utcnow().isoformat() + 'Z'

def display_binary_and_hash():
    """Continuously generates and displays binary representations and their hash codes."""
    while True:
        # Generate random binary string
        random_bytes = secrets.token_bytes(32)  # 32 random bytes
        random_binary = bin(int.from_bytes(random_bytes, 'big'))[2:]  # Convert to binary string
        random_hash = hashlib.sha256(random_bytes).hexdigest()  # Generate SHA-256 hash

        print(Fore.CYAN + f"Binary: {random_binary}, Hash: {random_hash}" + Style.RESET_ALL)
        time.sleep(0.5)  # Adjust refresh rate as needed

def main():
    count = 0
    keys_per_second = 100000  # Target number of keys to generate per second
    start_time = time.time()
    
    output_file = 'privatekey.json'
    keys_list = []  # List to store all private keys

    print(Fore.GREEN + "Generating private keys... (Press Ctrl+C to stop)\n" + Style.RESET_ALL)

    # Start the binary display and hash generation in a separate thread
    binary_hash_thread = threading.Thread(target=display_binary_and_hash, daemon=True)
    binary_hash_thread.start()

    try:
        while True:
            for _ in range(keys_per_second):
                private_key_bytes = generate_private_key()
                public_key_bytes = generate_public_key(private_key_bytes)

                # Generate hex representation
                private_key_hex = private_key_bytes.hex()
                private_key_hash = hashlib.sha256(private_key_bytes).hexdigest()
                public_key_hex = public_key_bytes.hex()

                # Prepare the complete metadata dictionary
                key_metadata = {
                    "private_key": private_key_hex  # Save in the new format
                }

                # Append the key metadata to the list
                keys_list.append(key_metadata)

                # Increment the count of keys generated
                count += 1
            
            elapsed_time = time.time() - start_time
            print(Fore.YELLOW + 
                  f"Generated {count} keys in {elapsed_time:.2f} seconds." + 
                  Style.RESET_ALL)

            # Introduce a slight delay to control the generation rate
            time.sleep(1)  # Adjust this if needed

    except KeyboardInterrupt:
        # Final output when the generation is stopped
        print(Fore.RED + 
              f"\nGeneration stopped. Total keys generated: {count}" +
              Style.RESET_ALL)

        # Write the collected private keys to the JSON file in the desired format
        try:
            with open(output_file, 'w') as file:
                json.dump(keys_list, file, indent=2)
            print(Fore.GREEN + f"Private keys saved to {output_file}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error saving private keys: {e}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()