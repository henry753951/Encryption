import json
from BaseEncryptAlgorithm import EncryptAlgorithm
from Algorithms.CenterOfGravityAlgorithm import CenterOfGravityAlgorithm
from Algorithms.MazeAlgorithm import MazeEncryption


key = "key"
Algorithms: list[EncryptAlgorithm] = [
    MazeEncryption(key, {"width": 25, "height": 25, "cheese": 10, "debug": False}),
    CenterOfGravityAlgorithm(key),
]


def decrypt(secret: str, key: str) -> str:
    for algorithm in list(reversed(Algorithms)):
        decrypted = algorithm.decrypt(secret)
        print(F"🔥🔥 演算法: {algorithm.__class__.__name__}")
        print(f"\tSecret: {secret}\n\tDecrypted: {decrypted}\n")
        secret = decrypted
    return secret


def encrypt(message: str, key: str) -> str:
    for algorithm in Algorithms:
        encrypted = algorithm.encrypt(message)
        print(F"🔥🔥 演算法: {algorithm.__class__.__name__}")
        print(f"\tMessage: {message}\n\tEncrypted: {encrypted}")
        message = encrypted
    return message


def error_handler(message, decrypted):
    with open("error.json", "w+") as f:
        try:
            errors: list = json.load(f)
            errors.append({"message": message, "decrypted": decrypted})
        except json.JSONDecodeError:
            errors = [{"message": message, "decrypted": decrypted}]
        json.dump(errors, f)

def test_errors():
    with open("error.json", "r") as f:
        errors: list = json.load(f)
        if not errors:
            return
    # TODO

if __name__ == "__main__":
    action = input("Action\n1. Encrypt\n2. Decrypt\n3. Test\n\nAction:")
    if action == "1":
        message = input("Message: ")
        encrypted = encrypt(message, key)
        print(f"❤️ Final Encrypted: {encrypted}")
    elif action == "2":
        secret = input("Secret: ")
        decrypted = decrypt(secret, key)
        print(f"❤️ Final Decrypted: {decrypted}\n\n")
    elif action == "3":
        with open("dataset.json", "r") as f:
            dataset = json.load(f)
        success = 0
        for message in dataset:
            print(f"🐳 Message: {message}")
            encrypted = encrypt(message, key)
            decrypted = decrypt(encrypted, key)
            if message != decrypted:
                print(f"❌ Error: {message} != {decrypted}")
                error_handler(message, decrypted)
            else:
                print(f"✅ Success: {message} == {decrypted}\n")
                success += 1
        print(f"🍈 Success: {success}/{len(dataset)}")
