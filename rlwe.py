from poly_utils import (
    create_poly_mod, poly_mul, poly_add, poly_sub, poly_neg, 
    sample_uniform, sample_error, bytes_to_bits, bits_to_bytes
)

class RLWECrypto:
    def __init__(self, n=1024, q=40961, std_dev=3.2):
        """
        Initialize RLWE cryptosystem parameters
        
        Args:
            n: Ring dimension (power of 2)
            q: Modulus (prime)
            std_dev: Standard deviation for error sampling
        """
        self.n = n
        self.q = q
        self.std_dev = std_dev
        
        # x^n + 1 is the irreducible polynomial for the quotient ring
        self.poly_mod = create_poly_mod(n)
    
    def generate_keypair(self):
        """
        Generate public and private keys
        
        Returns:
            tuple: (public_key, private_key)
        """
        a = sample_uniform(self.n, self.q)              # Sample polynomial a
        s = sample_error(self.n, self.q, self.std_dev)  # Private key
        e = sample_error(self.n, self.q, self.std_dev)  # Error
        
        # as = a*s mod (x^n + 1, q)
        as_poly = poly_mul(a, s, self.n, self.q)
        
        # b = -(a*s + e) mod q
        as_plus_e = poly_add(as_poly, e, self.q)
        b = poly_neg(as_plus_e, self.q)
        
        return ((a, b), s) # (public_key, private_key)
    
    def encrypt(self, public_key, message):
        """
        Encrypt a binary message
        
        Args:
            public_key: Public key (a, b)
            message: Binary polynomial message (encoded as coefficients of a polynomial)
        
        Returns:
            tuple: Ciphertext (c1, c2)
        """
        a, b = public_key
        
        
        r = sample_error(self.n, self.q, self.std_dev)  # Sample random polynomial r
        e1 = sample_error(self.n, self.q, self.std_dev) # Error for c1
        e2 = sample_error(self.n, self.q, self.std_dev) # Error for c2
        
        # Scale message to q/2
        scaled_message = [(bit * (self.q // 2)) % self.q for bit in message]
        
        # c1 = a*r + e1 mod (x^n + 1, q)
        ar = poly_mul(a, r, self.n, self.q)
        c1 = poly_add(ar, e1, self.q)
        
        # c2 = b*r + e2 + scaled_message mod (x^n + 1, q)
        br = poly_mul(b, r, self.n, self.q)
        br_e2 = poly_add(br, e2, self.q)
        c2 = poly_add(br_e2, scaled_message, self.q)
        
        return (c1, c2)
    
    def decrypt(self, private_key, ciphertext):
        """
        Decrypt a ciphertext
        
        Args:
            private_key: Private key s
            ciphertext: Ciphertext (c1, c2)
        
        Returns:
            list: Decrypted binary message
        """
        c1, c2 = ciphertext
        s = private_key
        
        # m' = c2 + c1*s mod (x^n + 1, q)
        c1s = poly_mul(c1, s, self.n, self.q)
        m_scaled = poly_add(c2, c1s, self.q)
        
        # Round to nearest multiple of q/2
        binary_msg = [0] * self.n
        for i in range(self.n):
            # If closer to q/2 than to 0, then bit is 1
            if m_scaled[i] > self.q // 4 and m_scaled[i] < 3 * self.q // 4:
                binary_msg[i] = 1
                
        return binary_msg
    
    def encode_message(self, message_str):
        """
        Encode a string message as a binary polynomial (pad with zeros if necessary)
        
        Args:
            message_str: String to encrypt
        
        Returns:
            list: Binary polynomial representation
        """
        message_bytes = message_str.encode('utf-8')
        bits = bytes_to_bits(message_bytes)
        
        binary_poly = [0] * self.n
        for i in range(min(len(bits), self.n)):
            binary_poly[i] = bits[i]
            
        return binary_poly
    
    def decode_message(self, binary_poly):
        """
        Decode a binary polynomial back to a string
        
        Args:
            binary_poly: Binary polynomial
        
        Returns:
            str: Decoded message
        """
        bytes_data = bits_to_bytes(binary_poly)    
        decoded = bytes_data.decode('utf-8', errors='ignore').rstrip('\x00')
        return decoded
