from BaseEncryptAlgorithm import EncryptAlgorithm
from MazeAlgorithm import MazeEncryption


key = "key"
Algorithms: list[EncryptAlgorithm] = [
    MazeEncryption(key, {"width": 25, "height": 25, "cheese": 10, "debug": True}),
]
action = input("Action (encrypt/decrypt): ")
if action == "decrypt":
    secret = input("Secret: ")
    for algorithm in Algorithms:
        decrypted = algorithm.decrypt(secret)
        print(f"Secret: {secret}\nDecrypted: {decrypted}\n")
        secret = decrypted
    print(f"Final Decrypted: {decrypted}")
else:
    message = input("Message: ")
    for algorithm in Algorithms:
        encrypted = algorithm.encrypt(message)
        print(f"Message: {message}\nEncrypted: {encrypted}")
        message = encrypted
    print(f"Final Encrypted: {encrypted}")
