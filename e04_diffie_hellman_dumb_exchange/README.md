# Diffie-Hellman key exchange - dumbed down version

## Overview

The Diffie-Hellman exchange is a means to secure a communication in a public space to avoid a third party eavesdrop on the conversation that is happening between the primary two talkers.

## The sequence

We will assume there are two primary exchangers (Alice and Bob) and one eavesdropper (Eve) → very original... I know...

The overall algorithm goes like this:
1. Alice generates a ***secret key*** (annotated **a**)
2. Bob generates a ***secret key*** (annotated **b**)
3. Alice and Bob agree on a ***common public key*** (annotated **p**)
4. Alice adds her secret key to the common public key to obtain ***Alice's public key*** (`X = a + p`)
5. Bob adds his secret key to the common public key to obtain ***Bob's public key*** (`Y = b + p`)
6. Alice and Bob exchange their combined keys (**X** goes to Bob and **Y** goes to Alice). Eve can sniff this exchange but she can't figure out **a** or **b** from **X** and **Y**, assuming this operation is extremely difficult to do
7. Alice adds her secret key to Bob's public key and obtains a ***common secret key*** (`K1 = Y + a`)
8. Bob adds his secret key to Alice's public key and obtains the same common secret key (`K2 = X + b`)
9. Bob and Alice now share a secret key that Eve doesn't know about (because **K1 equals K2**, or let's just call these **K**)
10. Communication starts, using **K** to encrypt and decrypt messages as symmetric cipher key

Beware that `a + p` and `b + p` are just dumbed down versions, whereas in the original Diffie-Hellman algorithm a more advanced mathematical expression is being used.

## Example

1. `alice_secret_key = 3`
2. `bob_secret_key = 7`
3. `common_public_key = 2`
4. `alice_public_key = alice_secret_key + common_public_key = 3 + 2 = 5`
5. `bob_public_key = bob_secret_key + common_public_key = 7 + 2 = 9`
6. Alice and Bob exchange their public keys
7. `alice_common_secret_key = bob_public_key + alice_secret_key = 9 + 3 = 12`
8. `bob_common_secret_key = alice_public_key + bob_secret_key = 5 + 7 = 12`

We can see that both Alice and Bob now share the same secret key **12**.
