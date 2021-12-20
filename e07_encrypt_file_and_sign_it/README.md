# File encryption

## Steps

1. Generate a symmetric key for the encryption of the data (the file)
2. Generate an asymmetric key pair for signing the file
3. Encrypt the file data
4. Generate a SHA256 hash for the encrypted data
5. Encrypt the hash with the private key
6. Serialize the encrypted data pieces into a file
7. Deserialize the encrypted file
8. Calculate the SHA256 hash of the encrypted data segment
9. Decrypt the signature segment of the encrypted file
10. Compare the hashes

## Format of the encrypted file

```
--- NEMEXIS ENCRYPTED ---
<2 byte | data segment length><1 byte | signature segment length>
--- END_HEADER ---
<actual data>
--- SIGNATURE ---
<signature data>
--- END ---
```
