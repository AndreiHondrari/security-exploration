import base64
import hashlib

from cryptography.hazmat.primitives import serialization as cser
from cryptography.exceptions import InvalidSignature

import nemexis_cipher


if __name__ == "__main__":

    # Get the keys
    with open("shared.key", "rb") as shared_pf:
        shared_key = shared_pf.read()

    shared_key = base64.b64decode(shared_key)
    shared_key = int.from_bytes(shared_key, 'big')

    print(f"Using shared key: {shared_key}\n")

    with open("sender_public.pem", "rb") as sender_pkey_pf:
        sender_pkey_raw = sender_pkey_pf.read()
        sender_pkey = cser.load_pem_public_key(sender_pkey_raw)

    print(f"Using public key for encryption: \n{sender_pkey_raw}\n")

    # Extract data pieces
    with open("output.enc", "rb") as encrypted_pf:
        HEADER = encrypted_pf.read(len(nemexis_cipher.HEADER))
        if (HEADER != nemexis_cipher.HEADER):
            print(
                f"Difference (HEADER): \n{HEADER}\n\n{nemexis_cipher.HEADER}"
            )
            exit(1)

        DATA_SEGMENT_LENGTH_B = encrypted_pf.read(2)
        SIGNATURE_SEGMENT_LENGTH_B = encrypted_pf.read(1)

        END_HEADER = encrypted_pf.read(len(nemexis_cipher.END_HEADER))
        if (END_HEADER != nemexis_cipher.END_HEADER):
            print(
                f"Difference (END_HEADER): \n{END_HEADER}\n\n"
                f"{nemexis_cipher.END_HEADER}")
            exit(1)

        DATA_SEGMENT = encrypted_pf.read(
            int.from_bytes(DATA_SEGMENT_LENGTH_B, 'big')
        )

        SIGNATURE = encrypted_pf.read(len(nemexis_cipher.SIGNATURE))
        if (SIGNATURE != nemexis_cipher.SIGNATURE):
            print(
                f"Difference (SIGNATURE): \n{SIGNATURE}\n\n"
                f"{nemexis_cipher.SIGNATURE}"
            )
            exit(1)

        SIGNATURE_SEGMENT = encrypted_pf.read(
            int.from_bytes(SIGNATURE_SEGMENT_LENGTH_B, 'big')
        )

        END = encrypted_pf.read(len(nemexis_cipher.END))
        if (END != nemexis_cipher.END):
            print(
                f"Difference (END): \n{END}\n\n"
                f"{nemexis_cipher.END}"
            )
            exit(1)

    # check signature validity
    counter_hash = hashlib.sha256(DATA_SEGMENT).digest()
    try:
        sender_pkey.verify(SIGNATURE_SEGMENT, counter_hash)
        print("--- SIGNATURE IS VALID")
    except InvalidSignature:
        print("ERROR: SIGNATURE IS NOT VALID!")
        exit(1)

    # decrypt data
    decrypted_data_segment = nemexis_cipher.decrypt(
        DATA_SEGMENT,
        shared_key
    )

    with open('decrypted.txt', 'w') as output:
        output.write(decrypted_data_segment.decode())

    print("--- FINISHED DECRYPTING")
