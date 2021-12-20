"""
An XOR symmetric stream cipher
"""

BLOCK_SIZE = 128
HEADER = "--- NEMEXIS ENCRYPTION ---\r\n".encode()
END_HEADER = "\r\n--- END_HEADER ---\r\n".encode()
SIGNATURE = "\r\n--- SIGNATURE ---\r\n".encode()
END = "\r\n--- END ---\r\n".encode()


def encrypt(original: bytes, shared_key: int) -> bytes:

    if len(original) == 0:
        return b''

    encrypted = b''
    for c in original:
        ec: int = c ^ shared_key
        encrypted += ec.to_bytes(1, 'big')

    return encrypted


def decrypt(encrypted: bytes, shared_key: int) -> bytes:
    if len(encrypted) == 0:
        return b''

    decrypted = b''
    for ec in encrypted:
        c = ec ^ shared_key
        decrypted += bytes([c])

    return decrypted
