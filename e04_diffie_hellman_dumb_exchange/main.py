import random
from dataclasses import dataclass
from typing import Optional


def get_rand(lower=1, upper=100):
    return random.randint(lower, upper + 1)


def encrypt_message(message, secret_key):
    # Using one-time pad (XOR) to encrypt
    output = [ord(char) ^ secret_key for char in message]
    return bytes(output)


def decrypt_message(message, secret_key):
    # Using one-time pad (XOR) to decrypt
    decrypted_characters = []
    for encrypted_char in message:
        decrypted_char = encrypted_char ^ secret_key
        decrypted_char = chr(decrypted_char)
        decrypted_characters.append(decrypted_char)

    return "".join(decrypted_characters)


if __name__ == "__main__":

    # define secrets for alice and bob
    alice_secret_key = get_rand()
    bob_secret_key = get_rand()
    print(f"Alice's secret key: {alice_secret_key}")
    print(f"Bob's secret key: {bob_secret_key}")

    # define common public value
    common_public_key = get_rand()
    print(f"Common key between alice and bob: {common_public_key}")

    # combine exchangeable keys to create public keys for Alice and Bob
    alice_public_key = alice_secret_key + common_public_key
    bob_public_key = bob_secret_key + common_public_key
    print(f"Alice's public key: {alice_public_key}")
    print(f"Bob's public key: {bob_public_key}")

    # ...exchange combined public keys between alice and bob
    print("Combined public keys are exchanged ...")

    # create common private key
    alice_common_secret_key = alice_secret_key + bob_public_key
    bob_common_secret_key = bob_secret_key + alice_public_key
    print(f"Alice's common secret key: {alice_common_secret_key}")
    print(f"Bob's common secret key: {bob_common_secret_key}")

    # begin actual secure communication, Alice sends encrypted message to Bob
    # to Eve, the actual message sent over the wire seems gibberish
    alice_message = "Hey Bob, how are you?"
    alice_encrypted_message = encrypt_message(
        alice_message,
        alice_common_secret_key  # alice uses her known common secret key
    )
    print(f"Alice sends \"{alice_encrypted_message}\"")

    # Bob decrypts Alice's message
    alice_decrypted_message = decrypt_message(
        alice_encrypted_message,
        bob_common_secret_key  # bob uses his known common secret key
    )
    print(f"Bob decrypts message to: \"{alice_decrypted_message}\"")

    # Bob sends back an encrypted reply
    bob_message = "I am eating a blueberry pie!"
    bob_encrypted_message = encrypt_message(
        bob_message,
        bob_common_secret_key  # bob uses his known common secret key
    )
    print(f"Bob sends \"{bob_encrypted_message}\"")

    # Alice decrypts Bob's message
    bob_decrypted_message = decrypt_message(
        bob_encrypted_message,
        alice_common_secret_key  # alice uses her known common secret key
    )
    print(f"Alice decrypts message to: \"{bob_decrypted_message}\"")
