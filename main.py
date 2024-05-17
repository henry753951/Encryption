from BaseEncryptAlgorithm import EncryptAlgorithm
from MazeAlgorithm import MazeEncryption


key = "key"
Algorithms: list[EncryptAlgorithm] = [
    MazeEncryption(key, {"width": 25, "height": 25, "cheese": 10, "debug": True}),
]
action = input("Action (encrypt/decrypt): ")
if action == "decrypt":
    for algorithm in Algorithms:
        secret = input("Secret: ")
        decrypted = algorithm.decrypt(secret)
        print(f"Secret: {secret}\nDecrypted: {decrypted}\n")
else:
    for algorithm in Algorithms:
        message = input("Message: ")
        encrypted = algorithm.encrypt(message)
        print(f"Message: {message}\nEncrypted: {encrypted}")
