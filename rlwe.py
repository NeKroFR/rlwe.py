from poly_utils import (
    Polynomial, create_poly_mod, poly_mul_mod, sample_uniform, 
    sample_error, bytes_to_bits, bits_to_bytes
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
        # Sample random polynomial a
        a = sample_uniform(self.n, self.q)
        
        # Sample small polynomials s and e
        s = sample_error(self.n, self.q, self.std_dev)  # Private key
        e = sample_error(self.n, self.q, self.std_dev)  # Error
        
        # Convert to Polynomial objects
        a_poly = Polynomial(a)
        s_poly = Polynomial(s)
        e_poly = Polynomial(e)
        
        # Compute public key b = -(a*s + e) mod q
        as_poly = poly_mul_mod(a_poly, s_poly, self.poly_mod, self.q)
        b_poly = (-as_poly - e_poly) % self.q
        b = b_poly.to_list(self.n)
        
        # Public key is (a, b), private key is s
        return ((a, b), s)
    
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
        
        # Sample random small r
        r = sample_error(self.n, self.q, self.std_dev)
        
        # Sample errors e1, e2
        e1 = sample_error(self.n, self.q, self.std_dev)
        e2 = sample_error(self.n, self.q, self.std_dev)
        
        # Convert to Polynomial objects
        a_poly = Polynomial(a)
        b_poly = Polynomial(b)
        r_poly = Polynomial(r)
        e1_poly = Polynomial(e1)
        e2_poly = Polynomial(e2)
        
        # Scale message to q/2
        scaled_message = []
        for bit in message:
            scaled_message.append((bit * (self.q // 2)) % self.q)
        scaled_message_poly = Polynomial(scaled_message)
        
        # Compute ciphertext
        c1_poly = (poly_mul_mod(a_poly, r_poly, self.poly_mod, self.q) + e1_poly) % self.q
        c2_poly = (poly_mul_mod(b_poly, r_poly, self.poly_mod, self.q) + e2_poly + scaled_message_poly) % self.q
        
        c1 = c1_poly.to_list(self.n)
        c2 = c2_poly.to_list(self.n)
        
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
        
        # Convert to Polynomial objects
        c1_poly = Polynomial(c1)
        c2_poly = Polynomial(c2)
        s_poly = Polynomial(s)
        
        # Compute m' = c2 + c1*s
        c1s_poly = poly_mul_mod(c1_poly, s_poly, self.poly_mod, self.q)
        m_scaled_poly = (c2_poly + c1s_poly) % self.q
        m_scaled = m_scaled_poly.to_list(self.n)
        
        # Round to nearest multiple of q/2
        binary_msg = [0] * self.n
        for i in range(self.n):
            # If closer to q/2 than to 0, then bit is 1
            if m_scaled[i] > self.q // 4 and m_scaled[i] < 3 * self.q // 4:
                binary_msg[i] = 1
                
        return binary_msg
    
    def encode_message(self, message_str):
        """
        Encode a string message as a binary polynomial
        
        Args:
            message_str: String to encrypt
        
        Returns:
            list: Binary polynomial representation
        """
        # Convert string to bytes, then to bits
        message_bytes = message_str.encode('utf-8')
        bits = bytes_to_bits(message_bytes)
        
        # Pad with zeros if necessary
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
        # Convert bits to bytes
        bytes_data = bits_to_bytes(binary_poly)
            
        # Convert bytes to string and strip any trailing null bytes/characters
        decoded = bytes_data.decode('utf-8', errors='ignore').rstrip('\x00')
        return decoded
