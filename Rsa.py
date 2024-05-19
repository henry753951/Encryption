import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

def generate_keypair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = mod_inverse(e, phi)
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    key, n = pk
    cipher = [(ord(char) ** key) % n for char in plaintext]
    return cipher

def decrypt(pk, ciphertext):
    key, n = pk
    plain = [chr((char ** key) % n) for char in ciphertext]
    return ''.join(plain)

# 示例
if __name__ == "__main__":
    # 选择两个素数 (注意：在实际应用中，这两个素数应该是非常大的)
    p = 61
    q = 53
    
    public, private = generate_keypair(p, q)
    print("Public Key:", public)
    print("Private Key:", private)
    
    message = "Hello, RSA!"
    encrypted_msg = encrypt(public, message)
    print("\nEncrypted Message:", encrypted_msg)
    
    decrypted_msg = decrypt(private, encrypted_msg)
    print("\nDecrypted Message:", decrypted_msg)
