import numpy as np
import random
import hashlib
import base64

from BaseEncryptAlgorithm import EncryptAlgorithm

DEBUG = False


def _print(*args, **kwargs):
    global DEBUG
    if DEBUG:
        print(*args, **kwargs)


class SubstitutionCipher(EncryptAlgorithm):
    def __init__(self, secret_key: str, options: dict = {}):
        super().__init__(secret_key)
        global DEBUG
        DEBUG = options.get("debug", False)
        self.sub_key1 = None
        self.sub_key2 = None
        self.sub_key3 = None
        self._generate_subkey()
        self.rails = None

    def _generate_subkey(self):
        # 將主密鑰轉換為32位URL安全的Base64編碼字節
        self.secret_key = self.secret_key.encode("utf-8")
        _print(self.secret_key)
        # 使用SHA-256計算散列值 並轉換為32位URL安全的Base64編碼字節
        self.sub_key1 = hashlib.sha256(self.secret_key).digest()
        _print(self.sub_key1)
        self.sub_key1 = base64.urlsafe_b64encode(self.sub_key1)
        _print(self.sub_key1)
        self.sub_key2 = hashlib.sha256(self.sub_key1).digest()
        self.sub_key2 = base64.urlsafe_b64encode(self.sub_key2)
        _print(self.sub_key2)
        self.sub_key3 = hashlib.sha256(self.sub_key2).digest()
        self.sub_key3 = base64.urlsafe_b64encode(self.sub_key3)
        _print(self.sub_key3)

    # 生成隨機替換字典
    def _create_substitution_map(self):
        random.seed(self.sub_key1)
        characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        random_characters = random.sample(characters, len(characters))  # 打亂順序
        substitution_map = dict(zip(characters, random_characters))  # 建立字典
        return substitution_map

    # 替換字典加密
    def _map_encrypt(self, plaintext):
        encrypted_message = ""
        substitution_map = self._create_substitution_map()
        for char in plaintext:
            if char in substitution_map:
                encrypted_message += substitution_map[char]
            else:
                encrypted_message += char
        return encrypted_message

    # 替換字典解密
    def _map_decrypt(self, secret):
        substitution_map = self._create_substitution_map()
        reversed_substitution_map = {v: k for k, v in substitution_map.items()}
        decrypted_message = ""
        for char in secret:
            if char in reversed_substitution_map:
                decrypted_message += reversed_substitution_map[char]
            else:
                decrypted_message += char
        return decrypted_message

    # 插入隨機字符加密(並記錄插入位置)
    def _insert_random_chars(self, plaintext):
        random.seed(self.sub_key2)
        characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        plaintext_list = list(plaintext)
        insert_positions = []
        for _ in range(random.randint(1, len(plaintext_list))):
            insert_position = random.randint(0, len(plaintext_list))
            random_char = random.choice(characters)
            plaintext_list.insert(insert_position, random_char)
            _print("".join(plaintext_list))
            insert_positions.append(str(insert_position).zfill(2))  # 轉換為2位數字串
        _print(insert_positions)
        for position in insert_positions:
            plaintext_list.append(position)  # 将插入位置信息添加到密文末尾
        _print("".join(plaintext_list))

        plaintext_list.append(
            str(len(insert_positions)).zfill(2)
        )  # 将插入字符的数量添加到密文末尾 轉成2位數字串

        return "".join(plaintext_list)

    # 插入隨機字符解密
    def _remove_random_chars(self, secret):
        secret_list = list(secret)
        num_inserted_chars = int("".join(secret_list[-2:]))  # 移除插入字符的數量 2位數字串
        secret_list = secret_list[:-2]
        insert_positions = []
        for _ in range(num_inserted_chars):
            # 移除插入位置信息 2位數字串
            position = int("".join(secret_list[-2:]))
            secret_list = secret_list[:-2]
            insert_positions.append(position)
        _print(insert_positions)
        for position in insert_positions:
            secret_list.pop(position)  # 移除插入的隨機字符
            _print("".join(secret_list))

        return "".join(secret_list)

    def _horizontal_queue_encrypt(self, plaintext):
        random.seed(self.sub_key3)
        self.rails = random.randint(3, 10)
        _print("Number of rails:", self.rails)
        fence = [[] for _ in range(self.rails)]
        rail = 0
        direction = 1

        for char in plaintext:
            _print(rail)
            fence[rail].append(char)
            rail += direction

            # 方向改變，在底端或頂端時改變方向
            if rail == self.rails - 1 or rail == 0:
                direction = -direction

        for rail in fence:
            _print(rail)
        # 由左至右，由上至下，將字符取出
        ciphertext = ""
        for rail in fence:
            ciphertext += "".join(rail)

        return ciphertext

    def _horizontal_queue_decrypt(self, ciphertext):
        random.seed(self.sub_key3)
        self.rails = random.randint(3, 10)
        fence = [[] for _ in range(self.rails)]
        rail = 0
        direction = 1

        fence_lengths = [0 for _ in range(self.rails)]
        fence_index = 0
        for _ in ciphertext:
            fence_lengths[fence_index] += 1
            fence_index += direction

            # 方向改變，在頂端或底端時改變方向
            if fence_index == self.rails - 1 or fence_index == 0:
                direction = -direction

        # 從密文中按照順序取出字符，放入對應位置
        index = 0
        for i in range(self.rails):
            for _ in range(fence_lengths[i]):
                fence[i].append(ciphertext[index])
                index += 1
        plaintext = ""
        rail = 0
        direction = 1
        for _ in range(len(ciphertext)):
            plaintext += fence[rail].pop(0)
            rail += direction

            # 方向改變，在頂端或底端時改變方向
            if rail == self.rails - 1 or rail == 0:
                direction = -direction

        return plaintext

    def encrypt(self, plaintext):

        # 插入隨機字符加密
        _print("INSERT RANDOM CHARACTERS")
        encrypted_message = self._insert_random_chars(plaintext)
        _print(plaintext)

        # 替換字符加密
        _print("\nSUBSTITUTION CIPHER")
        encrypted_message = self._map_encrypt(encrypted_message)
        _print(encrypted_message)

        # 柵欄加密
        _print("\nHORIZONTAL QUEUE ENCRYPTION")
        encrypted_message = self._horizontal_queue_encrypt(encrypted_message)
        _print(encrypted_message)

        return encrypted_message

    def decrypt(self, secret):
        # 柵欄解密
        _print("\nRAIL FENCE DECRYPTION")
        decrypted_message = self._horizontal_queue_decrypt(secret)
        _print(decrypted_message)

        # 替換字符解密
        _print("\nSUBSTITUTION DECRYPTION")
        decrypted_message = self._map_decrypt(decrypted_message)
        _print(decrypted_message)

        # 隨機插入字符解密
        _print("\nREMOVE RANDOM CHARACTERS")
        decrypted_message = self._remove_random_chars(decrypted_message)
        _print(decrypted_message)

        return decrypted_message


if __name__ == "__main__":
    cipher = SubstitutionCipher("PIYAN", {"debug": True})

    message = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    encrypted_message = cipher.encrypt(message)
    decrypted_message = cipher.decrypt(encrypted_message)
    print("\nEncrypted message:", encrypted_message)
    print("Decrypted message:", decrypted_message)
