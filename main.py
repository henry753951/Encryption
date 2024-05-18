import json
from BaseEncryptAlgorithm import EncryptAlgorithm
from Algorithms.CenterOfGravityAlgorithm import CenterOfGravityAlgorithm
from Algorithms.MazeAlgorithm import MazeEncryption


key = "key"
Algorithms: list[EncryptAlgorithm] = [
    MazeEncryption(key, {"width": 25, "height": 25, "cheese": 10, "debug": False}),
    CenterOfGravityAlgorithm(key),
]


def decrypt(secret: str) -> str:
    for algorithm in list(reversed(Algorithms)):
        decrypted = algorithm.decrypt(secret)
        print(F"  🔑 演算法: {algorithm.__class__.__name__}")
        print(f"\tSecret: {secret}\n\tDecrypted: {decrypted}")
        secret = decrypted
    return secret


def encrypt(message: str) -> tuple[str, list[dict]]:
    each_inputs = []
    for algorithm in Algorithms:
        encrypted = algorithm.encrypt(message)
        each_inputs.append(
            {"message": message, "encrypted": encrypted, "algorithm": algorithm.__class__.__name__}
        )
        print(F"  🔒 演算法: {algorithm.__class__.__name__}")
        print(f"\tMessage: {message}\n\tEncrypted: {encrypted}")
        message = encrypted
    return (message, each_inputs)


def error_handler(message, each_inputs):
    with open("error.json", "r") as f:
        try:
            errors: list = json.load(f)
        except json.JSONDecodeError:
            errors = []
        errors.append({"message": message, "each_inputs": each_inputs})
    with open("error.json", "w") as f:
        json.dump(errors, f)


def test_errors():
    with open("error.json", "r") as f:
        errors: list = json.load(f)
        if not errors:
            return
    print("########## Error Test ############")
    print(f"🍈 Errors: {len(errors)}")
    for algorithm in list(Algorithms):
        print(f"🔒 Algorithm: {algorithm.__class__.__name__}")
        for error in errors:
            for index, each_input in enumerate(error["each_inputs"]):
                if each_input["algorithm"] == algorithm.__class__.__name__:
                    print(f"\tMessage: {each_input['message']}")
                    print(f"\tEncrypted: {each_input['encrypted']}")
                    decrypted = Algorithms[index].decrypt(each_input["encrypted"])
                    if each_input["message"] != decrypted:
                        print(f"\t❌ Error: {each_input['message']} != {decrypted}")
                    elif each_input["message"] == decrypted:
                        print("\t✅ Success")
        print("\n")


if __name__ == "__main__":
    action = input("Action\n1. Encrypt\n2. Decrypt\n3. Test\n\nAction:")
    if action == "1":
        message = input("Message: ")
        encrypted = encrypt(message)[0]
        print(f"❤️ Final Encrypted: {encrypted}")
    elif action == "2":
        secret = input("Secret: ")
        decrypted = decrypt(secret)
        print(f"❤️ Final Decrypted: {decrypted}\n\n")
    elif action == "3":
        with open("dataset.json", "r") as f:
            dataset = json.load(f)
        with open("error.json", "w") as f:
            json.dump([], f)
        success = 0
        for message in dataset:
            try:
                print(f"🐳 Message: {message}")
                encrypted, each_inputs = encrypt(message)
                decrypted = decrypt(encrypted)
                if message != decrypted:
                    print(f"❌ Error: {message} != {decrypted}")
                    error_handler(message, each_inputs)
                else:
                    print(f"✅ Success: {message} == {decrypted}\n")
                    success += 1
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌❌❌ Error: {e}")
                error_handler(message, each_inputs)
        print(f"\n\n🍈 Success: {success}/{len(dataset)}")

        test_errors()
