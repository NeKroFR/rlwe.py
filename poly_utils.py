import random

def create_poly_mod(n):
    """
    Create the polynomial modulus x^n + 1.
    
    Args:
        n (int): Ring dimension
        
    Returns:
        list: Polynomial coefficients representing x^n + 1
    """
    coeffs = [1] + [0] * (n - 1) + [1]  # x^n + 1
    return coeffs

def poly_add(a, b, q):
    """
    Add two polynomials modulo q.
    
    Args:
        a (list): First polynomial coefficients (length n)
        b (list): Second polynomial coefficients (length n)
        q (int): Modulus
        
    Returns:
        list: Resulting polynomial coefficients (length n)
    """
    n = len(a)
    return [(a[i] + b[i]) % q for i in range(n)]

def poly_sub(a, b, q):
    """
    Subtract two polynomials modulo q.
    
    Args:
        a (list): First polynomial coefficients (length n)
        b (list): Second polynomial coefficients (length n)
        q (int): Modulus
        
    Returns:
        list: Resulting polynomial coefficients (length n)
    """
    n = len(a)
    return [(a[i] - b[i] + q) % q for i in range(n)]

def poly_neg(a, q):
    """
    Negate a polynomial modulo q.
    
    Args:
        a (list): Polynomial coefficients (length n)
        q (int): Modulus
        
    Returns:
        list: Resulting polynomial coefficients (length n)
    """
    n = len(a)
    return [(q - a[i]) % q for i in range(n)]

def poly_mul(a, b, n, q):
    """
    Multiply two polynomials in the ring Z_q[x]/(x^n + 1) using negacyclic convolution.
    
    Args:
        a (list): First polynomial coefficients (length n)
        b (list): Second polynomial coefficients (length n)
        n (int): Polynomial degree (ring dimension)
        q (int): Modulus
        
    Returns:
        list: Resulting polynomial coefficients (length n)
    """
    result = [0] * n
    for i in range(n):
        for j in range(n):
            k = (i + j) % n
            sign = 1 if (i + j) < n else -1
            term = (a[i] * b[j]) % q
            if sign == 1:
                result[k] = (result[k] + term) % q
            else:
                result[k] = (result[k] + q - term) % q
    return result

def randbelow(n):
    """
    Generate a random integer in [0, n-1] using atomic operations for Verilog compatibility.
    
    Args:
        n (int): Upper bound (n > 0)
        
    Returns:
        int: Random number in [0, n-1]
    """
    if n <= 0:
        raise ValueError("Upper bound must be positive")
    
    bits = 0
    tmp = n - 1
    while tmp > 0:
        bits += 1
        tmp >>= 1
    
    mask = (1 << bits) - 1
    
    while True:
        r = 0
        for i in range(bits):
            bit = random.randint(0, 1)
            r |= (bit << i)
        
        if r < n:
            return r

def sample_uniform(n, q):
    """
    Sample a uniform polynomial from Z_q[x].
    
    Args:
        n (int): Number of coefficients
        q (int): Modulus
        
    Returns:
        list: Polynomial coefficients (length n)
    """
    return [randbelow(q) for _ in range(n)]

def sample_error(n, q, std_dev):
    """
    Sample an error polynomial from a discrete Gaussian distribution.
    
    Args:
        n (int): Number of coefficients
        q (int): Modulus
        std_dev (float): Standard deviation
        
    Returns:
        list: Polynomial coefficients (length n)
    """
    return [round(random.gauss(0, std_dev)) % q for _ in range(n)]

def bytes_to_bits(byte_data):
    """
    Convert bytes to a list of bits.
    
    Args:
        byte_data (bytes): Input byte data
        
    Returns:
        list: List of bits
    """
    result = []
    for b in byte_data:
        for i in range(8):
            result.append((b >> i) & 1)
    return result

def bits_to_bytes(bits):
    """
    Convert a list of bits to bytes.
    
    Args:
        bits (list): List of bits
        
    Returns:
        bytearray: Resulting bytes
    """
    bytes_data = bytearray()
    for i in range(0, len(bits), 8):
        if i + 8 > len(bits):
            break
        byte = 0
        for j in range(8):
            if i + j < len(bits):
                byte |= bits[i + j] << j
        bytes_data.append(byte)
    return bytes_data
