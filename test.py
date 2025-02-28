from rlwe import RLWECrypto

if __name__ == "__main__":
    rlwe = RLWECrypto(n=1024, q=40961, std_dev=3.2)    
    plaintext = "Hello, Ring-LWE cryptography!"
    print(f"Original message: {plaintext}")
    
    print("Generating keypair...")
    public_key, private_key = rlwe.generate_keypair()
    print("Keypair generated.")
    print(f"Public key (truncated): a[0:5]={public_key[0][:5]}, b[0:5]={public_key[1][:5]}")
    print(f"Private key (truncated): s[0:5]={private_key[:5]}")
    #print(f"Public key: a={public_key[0]}, b={public_key[1]}")
    #print(f"Private key: s={private_key}")

    print("Encoding message as binary polynomial...")
    binary_message = rlwe.encode_message(plaintext)
    print(f"Message encoded as binary polynomial with {len(binary_message)} coefficients")

    print("Encrypting message...")
    ciphertext = rlwe.encrypt(public_key, binary_message)
    print("Message encrypted.")
    print(f"Ciphertext (truncated): c1[0:5]={ciphertext[0][:5]}, c2[0:5]={ciphertext[1][:5]}")
    #print(f"Ciphertext: c1={ciphertext[0]}, c2={ciphertext[1]}")
    
    
    print("Decrypting message...")
    decrypted_binary = rlwe.decrypt(private_key, ciphertext)
    decrypted_message = rlwe.decode_message(decrypted_binary)
    print(f"Decrypted message: {decrypted_message}")
    
    if plaintext == decrypted_message:
        print("SUCCESS: Decryption successful!")
    else:
        print("FAILURE: Decryption failed!")
        print(f"Original: {plaintext}")
        print(f"Decrypted: {decrypted_message}")
