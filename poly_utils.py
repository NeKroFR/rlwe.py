import random

class Polynomial:
    def __init__(self, coefficients=None, degree=None):
        # Initialize a polynomial with given coefficients or zeros if degree is specified
        if coefficients is not None:
            self.coefficients = list(coefficients)
            while len(self.coefficients) > 1 and self.coefficients[-1] == 0:
                self.coefficients.pop()
        elif degree is not None:
            self.coefficients = [0] * (degree + 1)
        else:
            self.coefficients = [0]
    
    def __getitem__(self, index):
        # Get coefficient at index
        if index < len(self.coefficients):
            return self.coefficients[index]
        return 0
    
    def __setitem__(self, index, value):
        # Set coefficient at index
        if index >= len(self.coefficients):
            self.coefficients.extend([0] * (index - len(self.coefficients) + 1))
        self.coefficients[index] = value
    
    def __len__(self):
        # Get number of coefficients
        return len(self.coefficients)
    
    def degree(self):
        # Get degree of polynomial
        return len(self.coefficients) - 1
    
    def __add__(self, other):
        # Add two polynomials
        if isinstance(other, (int, float)):
            result = Polynomial(self.coefficients.copy())
            result[0] += other
            return result
        
        result_degree = max(self.degree(), other.degree())
        result = Polynomial(degree=result_degree)
        
        for i in range(result_degree + 1):
            result[i] = self[i] + other[i]
        
        return result
    
    def __sub__(self, other):
        # Subtract polynomial
        if isinstance(other, (int, float)):
            result = Polynomial(self.coefficients.copy())
            result[0] -= other
            return result
        
        result_degree = max(self.degree(), other.degree())
        result = Polynomial(degree=result_degree)
        
        for i in range(result_degree + 1):
            result[i] = self[i] - other[i]
        
        return result
    
    def __neg__(self):
        # Negate polynomial
        return Polynomial([-c for c in self.coefficients])
    
    def __mul__(self, other):
        # Multiply polynomials
        if isinstance(other, (int, float)):
            return Polynomial([c * other for c in self.coefficients])
        
        result_degree = self.degree() + other.degree()
        result = Polynomial(degree=result_degree)
        
        for i in range(self.degree() + 1):
            for j in range(other.degree() + 1):
                result[i + j] += self[i] * other[j]
        
        return result
    
    def __mod__(self, modulus):
        # Take coefficients modulo a number
        if isinstance(modulus, (int, float)):
            return Polynomial([c % modulus for c in self.coefficients])
        elif isinstance(modulus, Polynomial):
            return polynomial_mod(self, modulus)
        
        raise TypeError("Modulus must be a number or polynomial")
    
    def to_list(self, length=None):
        # Convert to list of coefficients with specified length
        if length is None:
            return self.coefficients.copy()
        
        result = self.coefficients.copy()
        if len(result) < length:
            result.extend([0] * (length - len(result)))
        elif len(result) > length:
            result = result[:length]
        
        return result
    
    def __str__(self):
        # String representation of the polynomial
        if not self.coefficients or all(c == 0 for c in self.coefficients):
            return "0"
            
        terms = []
        for i, c in enumerate(self.coefficients):
            if c == 0:
                continue
                
            if i == 0:
                terms.append(str(c))
            elif i == 1:
                if c == 1:
                    terms.append("x")
                elif c == -1:
                    terms.append("-x")
                else:
                    terms.append(f"{c}x")
            else:
                if c == 1:
                    terms.append(f"x^{i}")
                elif c == -1:
                    terms.append(f"-x^{i}")
                else:
                    terms.append(f"{c}x^{i}")
        
        return " + ".join(terms).replace(" + -", " - ")

def polynomial_mod(dividend, divisor):
    """
    Compute polynomial remainder when dividend is divided by divisor
    """
    # Create a copy of the dividend
    remainder = Polynomial(dividend.coefficients.copy())
    divisor_degree = divisor.degree()
    divisor_leading = divisor[divisor_degree]
    
    # Continue until remainder's degree is less than divisor's
    while remainder.degree() >= divisor_degree and not all(c == 0 for c in remainder.coefficients):
        # Calculate the leading term of the quotient
        remainder_degree = remainder.degree()
        if remainder_degree < divisor_degree:
            break
            
        # Calculate coefficient and exponent of the leading term of quotient
        coefficient = remainder[remainder_degree] / divisor_leading
        exponent = remainder_degree - divisor_degree
        
        # Subtract divisor * leading term from remainder
        for i in range(divisor_degree + 1):
            remainder[i + exponent] -= coefficient * divisor[i]
        
        # Trim trailing zeros
        while len(remainder.coefficients) > 1 and abs(remainder.coefficients[-1]) < 1e-10:
            remainder.coefficients.pop()

    return remainder

def create_poly_mod(n):
    # Create the polynomial x^n + 1 for RLWE
    result = Polynomial(degree=n)
    result[0] = 1
    result[n] = 1
    return result

def poly_mul_mod(a, b, mod_poly, q):
    """
    Multiply two polynomials in the ring R_q = Z_q[x]/(mod_poly)
    Args:
        a, b: Polynomial objects or coefficient lists
        mod_poly: The modulus polynomial (e.g., x^n + 1)
        q: Coefficient modulus
    """
    if not isinstance(a, Polynomial):
        a = Polynomial(a)
    if not isinstance(b, Polynomial):
        b = Polynomial(b)
    
    result = (a * b) % mod_poly
    
    for i in range(len(result.coefficients)):
        result.coefficients[i] = round(result.coefficients[i]) % q
    
    return result

def randbelow(n):
    """
    Generate a random integer in the range [0, n-1]
    """
    # Generate random bytes with enough entropy
    num_bytes = (n.bit_length() + 7) // 8
    # Convert to int and ensure it's below n
    r = int.from_bytes(random.getrandbits(num_bytes * 8).to_bytes(num_bytes, 'big'), 'big')
    # Modulo bias is negligible for cryptographic purposes when n is large
    return r % n

def sample_uniform(n, q):
    # Sample uniformly from R_q (polynomials with coefficients in Z_q)
    return [randbelow(q) for _ in range(n)]

def sample_error(n, q, std_dev):
    # Sample from error distribution (discrete Gaussian)
    return [round(random.gauss(0, std_dev)) % q for _ in range(n)]

def bytes_to_bits(byte_data):
    # Convert bytes to a list of bits
    result = []
    for b in byte_data:
        for i in range(8):
            result.append((b >> i) & 1)
    return result

def bits_to_bytes(bits):
    # Convert a list of bits to bytes
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
