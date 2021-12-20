import secrets
import base64

from cryptography.hazmat.primitives import serialization as cser
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


if __name__ == "__main__":

    # Generate symmetric key for the file encryption
    print("Generating shared key ...")
    shared_key_i = 0

    while shared_key_i == 0:
        shared_key_i = secrets.randbits(8)

    shared_key = base64.b64encode(shared_key_i.to_bytes(1, 'big'))

    print(f"Generated shared: {shared_key_i}")
    with open("shared.key", "wb") as shared_key_pf:
        shared_key_pf.write(shared_key)

    # Generate asymmetric keys
    print("Generating asymmetric key pair ...")
    ed_skey = Ed25519PrivateKey.generate()
    sender_sk = ed_skey.private_bytes(
        cser.Encoding.PEM,
        cser.PrivateFormat.PKCS8,
        cser.NoEncryption()
    )

    ed_pkey = ed_skey.public_key()
    sender_pk = ed_pkey.public_bytes(
        cser.Encoding.PEM,
        cser.PublicFormat.SubjectPublicKeyInfo,
    )

    with open("sender_private.pem", "wb") as sender_sk_pf:
        sender_sk_pf.write(sender_sk)

    with open("sender_public.pem", "wb") as sender_pk_pf:
        sender_pk_pf.write(sender_pk)
