import base64
import hashlib

from cryptography.hazmat.primitives import serialization as cser

import nemexis_cipher


if __name__ == "__main__":

    # Get the keys
    with open("shared.key", "rb") as shared_pf:
        shared_key = shared_pf.read()

    shared_key = base64.b64decode(shared_key)
    shared_key = int.from_bytes(shared_key, 'big')

    print(f"Using shared key: {shared_key}\n")

    with open("sender_private.pem", "rb") as sender_skey_pf:
        sender_skey_raw = sender_skey_pf.read()
        sender_skey = cser.load_pem_private_key(sender_skey_raw, None)

    print(f"Using private key for encryption: \n{sender_skey_raw}\n")

    # Encrypt file
    # notice the file is opened in binary mode because we ignore the extension
    with open("original_file.txt", "rb") as original_pf:
        original = original_pf.read()
        print(f"Original message: \n{original[:250]} ...")

    encrypted = nemexis_cipher.encrypt(original, shared_key)

    print(f"Encrypted message: \n{encrypted[:250]} ...")

    # Generate hash of the encrypted message
    encrypted_message_digest = hashlib.sha256(encrypted).digest()

    # Encrypt the hash
    signature = sender_skey.sign(encrypted_message_digest)

    output = b''

    # header
    output += nemexis_cipher.HEADER
    output += (len(encrypted)).to_bytes(2, 'big')
    output += (len(signature)).to_bytes(1, 'big')
    output += nemexis_cipher.END_HEADER

    # data
    output += encrypted

    # signature
    output += nemexis_cipher.SIGNATURE
    output += signature
    output += nemexis_cipher.END

    # Output the encrypted file
    with open("output.enc", "wb") as output_pf:
        output_pf.write(output)
