# Minimalist RLWE Cryptography in Python

This project is an implementation of the Ring Learning With Errors (RLWE) encryption scheme.
It demonstrates key generation, encryption, and decryption based on polynomial arithmetic in the ring R₍q₎ = ℤ₍q₎[x]/(xⁿ + 1).

## Overview

- **RLWE Fundamentals:**  
  RLWE leverages the hardness of solving noisy linear equations in polynomial rings. Here, the ring is defined as R₍q₎ = ℤ₍q₎[x]/(xⁿ + 1) with:
  - **n:** Ring dimension (a power of 2)
  - **q:** A prime modulus

- **Key Operations:**  
  - **Key Generation:**  
    - Private key: A small error polynomial *s*.
    - Public key: A pair *(a, b)* where *a* is uniformly random and *b = -(a·s + e)* (mod *q*).
  - **Encryption:**  
    - Message (as a binary polynomial) is scaled and added to the product of *b* and a random small polynomial *r*, plus additional error.
    - Ciphertext: *(c₁, c₂)*.
  - **Decryption:**  
    - Recovers the message by computing *c₂ + c₁·s* (mod *q*) and then rounding the result.

## File Structure

- **`poly_utils.py`:**  
  Provides polynomial arithmetic (addition, multiplication, modular reduction) and utility functions (sampling and bit conversion).

- **`rlwe.py`:**  
  Implements RLWE operations including key generation, encryption, decryption, and message encoding/decoding.

- **`test.py`:**  
  Contains a demonstration of the encryption/decryption process.

## Usage Example

```python
from rlwe import RLWECrypto

# Initialize with 128-bit security parameters
rlwe = RLWECrypto(n=1024, q=40961, std_dev=3.2)

# Generate keypair
public_key, private_key = rlwe.generate_keypair()

# Encrypt a message
message = "Hello, Ring-LWE!"
binary_message = rlwe.encode_message(message)
ciphertext = rlwe.encrypt(public_key, binary_message)

# Decrypt the ciphertext
decrypted_binary = rlwe.decrypt(private_key, ciphertext)
decrypted_message = rlwe.decode_message(decrypted_binary)
print(decrypted_message)
```

## Security Parameters

| Security Level | n    | q      | std_dev |
|----------------|------|--------|---------|
| 128-bit        | 1024 | 40961  | 3.2     |
| 192-bit        | 2048 | 65537  | 3.2     |
| 256-bit        | 4096 | 114689 | 4.0     |

*Adjust parameters based on your security requirements.*
