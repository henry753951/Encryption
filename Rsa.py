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

# def encrypt(pk, plaintext):
#     key, n = pk
#     cipher = [(ord(char) ** key) % n for char in plaintext]
#     return cipher

# def decrypt(pk, ciphertext):
#     key, n = pk
#     plain = [chr((char ** key) % n) for char in ciphertext]
#     return ''.join(plain)

def encrypt(plain_text, public_key):
    e, n = public_key
    cipher_text = [pow(ord(char), e, n) for char in plain_text]
    return cipher_text

def decrypt(cipher_text, private_key):
    d, n = private_key
    plain_text = [chr(pow(char, d, n)) for char in cipher_text]
    return ''.join(plain_text)

# 示例
if __name__ == "__main__":
    # 选择两个素数 (注意：在实际应用中，这两个素数应该是非常大的)
    p = 61
    q = 53

    # 計算 n 和 φ(n)
    n = p * q
    phi = (p - 1) * (q - 1)

    # 自訂公鑰 (e, n)
    e = 17  # 一般選擇 65537，但這裡選擇一個小值方便計算
    # 計算私鑰 d
    d = pow(e, -1, phi)

    # 公鑰和私鑰
    public_key = (e, n)
    private_key = (d, n)
    # print("public: "+str(public_key)+'\n')
    # print("private: "+str(private_key)+'\n')
    
    action = input("Action\n1. Encrypt\n2. Decrypt\n\nAction:")
    if action == "1":
        message = input("Message: ")
        encrypted = encrypt(message, public_key)
        print("Encrypted: ", encrypted)
        print("public: "+str(public_key)+'\n')
    elif action == "2":
        e = int(input("Public key 'e': "))
        n = input("Public key 'N': ")
        
        secret = input("Secret: ")
        input_str = secret.strip('[]').replace(' ', '')
        
        output_list = [int(num) for num in input_str.split(',')]
        print(output_list)
        decrypted = decrypt(output_list, private_key)
        print("Decrypted: ", decrypted)
    
    # # 原始訊息
    # message = "HELLO"

    # # 加密過程
    # encrypted_message = encrypt(message, public_key)
    # print("Encrypted message:", encrypted_message)

    # # 解密過程
    # decrypted_message = decrypt(encrypted_message, private_key)
    # print("Decrypted message:", decrypted_message)
