import random
import math
from BaseEncryptAlgorithm import EncryptAlgorithm


class CenterOfGravityAlgorithm(EncryptAlgorithm):
    def __init__(self, secret_key: str) -> None:
        super().__init__(secret_key)
        self.char_map = {
            'A': (0, 0),
            'B': (3, 0),
            'C': (6, 0),
            'D': (9, 0),
            'E': (12, 0),
            'F': (15, 0),
            'G': (18, 0),
            'H': (21, 0),
            'I': (24, 0),
            'J': (27, 0),
            'K': (30, 0),
            'L': (33, 0),
            'M': (36, 0),
            'N': (39, 0),
            'O': (42, 0),
            'P': (45, 0),
            'Q': (48, 0),
            'R': (51, 0),
            'S': (54, 0),
            'T': (57, 0),
            'U': (60, 0),
            'V': (63, 0),
            'W': (66, 0),
            'X': (69, 0),
            'Y': (72, 0),
            'Z': (75, 0),
            'a': (0, 3),
            'b': (3, 3),
            'c': (6, 3),
            'd': (9, 3),
            'e': (12, 3),
            'f': (15, 3),
            'g': (18, 3),
            'h': (21, 3),
            'i': (24, 3),
            'j': (27, 3),
            'k': (30, 3),
            'l': (33, 3),
            'm': (36, 3),
            'n': (39, 3),
            'o': (42, 3),
            'p': (45, 3),
            'q': (48, 3),
            'r': (51, 3),
            's': (54, 3),
            't': (57, 3),
            'u': (60, 3),
            'v': (63, 3),
            'w': (66, 3),
            'x': (69, 3),
            'y': (72, 3),
            'z': (75, 3),
            '0': (0, 6),
            '1': (3, 6),
            '2': (6, 6),
            '3': (9, 6),
            '4': (12, 6),
            '5': (15, 6),
            '6': (18, 6),
            '7': (21, 6),
            '8': (24, 6),
            '9': (27, 6),
        }
        self.encrypt_char_x_map = {
            'A': 0,
            'B': 1,
            'C': 2,
            'D': 3,
            'E': 4,
            'F': 5,
            'G': 6,
            'H': 7,
            'I': 8,
            'J': 9,
            'K': 10,
            'L': 11,
            'M': 12,
            'N': 13,
            'O': 14,
            'P': 15,
            'Q': 16,
            'R': 17,
            'S': 18,
            'T': 19,
            'U': 20,
            'V': 21,
            'W': 22,
            'X': 23,
            'Y': 24,
            'Z': 25,
        }
        self.encrypt_char_y_map = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6}
        self.key_point = self.generate_sequence(self.secret_key, 2)

    def generate_sequence(self, seed, length):
        random.seed(seed)  # 設置隨機種子
        sequence = []
        for _ in range(length):
            choise_x = random.choice(
                [
                    0,
                    3,
                    6,
                    9,
                    12,
                    15,
                    18,
                    21,
                    24,
                    27,
                    30,
                    33,
                    36,
                    39,
                    42,
                    45,
                    48,
                    51,
                    54,
                    57,
                    60,
                    63,
                    66,
                    69,
                    72,
                    75,
                ]
            )
            choice_y = random.choice([0, 3, 6])
            if choice_y == 6:
                choise_x = random.choice([0, 3, 6, 9, 12, 15, 18, 21, 24, 27])
            sequence.append((choise_x, choice_y))
        return sequence

    def encrypt(self, text):
        (x1, y1) = self.key_point[0]
        (x2, y2) = self.key_point[1]
        encrypted_text = ""
        for char in text:
            x, y = self.char_map[char]
            new_x = (x + x1 + x2) / 3
            new_y = (y + y1 + y2) / 3
            for c in self.encrypt_char_x_map:
                if new_x % 26 == self.encrypt_char_x_map[c]:
                    for d in self.encrypt_char_y_map:
                        if new_y % 7 == self.encrypt_char_y_map[d]:
                            encrypted_text += c + d
                            break
                    break
        return encrypted_text

    def decrypt(self, encrypted_text):
        (x1, y1) = self.key_point[0]
        (x2, y2) = self.key_point[1]
        decrypted_text = ""
        for char in range(0, len(encrypted_text), 2):
            x = self.encrypt_char_x_map[encrypted_text[char]]
            y = self.encrypt_char_y_map[encrypted_text[char + 1]]
            if x * 3 - x1 - x2 < 0:
                x = x + 26
            new_x = x * 3 - x1 - x2
            if y * 3 - y1 - y2 < 0:
                y = y + 7
            new_y = y * 3 - y1 - y2
            for c in self.char_map:
                if self.char_map[c] == (new_x, new_y):
                    decrypted_text += c
                    break
        return decrypted_text

