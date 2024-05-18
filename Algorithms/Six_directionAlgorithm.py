from Map import MAP, __MAP__, __Mose__MAP__
from BaseEncryptAlgorithm import EncryptAlgorithm

import random
class Six_directionAlgorithm(EncryptAlgorithm):
    def __init__(self, secret_key: str ) -> None:
        super().__init__(secret_key)
        self.seed = "2" + secret_key
        self.length = 5
        self.SECRET = secret_key[0:5]

    def decrypt(self, secret: str) -> str:
        secret = list(secret)
        de_first_key = [Six_directionAlgorithm.generate_sequence(self.seed, self.length)]
        de_second_key = [[],[],[],[],[]]

        de_morse_second_key = []
        de_TEXT_morse_second_key = ""
        for i in range(len(self.SECRET)):
            de_morse_second_key.append(__Mose__MAP__[self.SECRET[i]])

        # print(morse_second_key)
        for i in range(len(de_morse_second_key)):
            for j in range(len(de_morse_second_key[i])):
                de_TEXT_morse_second_key += str(de_morse_second_key[i][j])

        # 間隔抓key 例如[[0, 0, 2, 2, 1], [0, 0, 0, 0, 2], [0, 0, 1, 2, 1]]  -> [[0, 0, 0], [0, 0, 0], [2, 0, 1], [2, 0, 2], [1, 2, 1]]
        for i in range(len(de_TEXT_morse_second_key)):
            if i % 5 == 0:
                de_second_key[0].append(de_TEXT_morse_second_key[i])
            elif i % 5 == 1:
                de_second_key[1].append(de_TEXT_morse_second_key[i])
            elif i % 5 == 2:
                de_second_key[2].append(de_TEXT_morse_second_key[i])
            elif i % 5 == 3:
                de_second_key[3].append(de_TEXT_morse_second_key[i])
            elif i % 5 == 4:
                de_second_key[4].append(de_TEXT_morse_second_key[i])
        de_substitute = []
        for i in range(len(secret)):
            # for j in range(len(first_key)):
                # print("sscc",first_key[j])
            de_substitute.append(Six_directionAlgorithm.de_how_to_go([secret[i]],de_first_key[0],de_second_key[i]))
        # print("解密回來後 : ",de_substitute)
        
        cout = ""
        for i in range(len(de_substitute)):
            cout += de_substitute[i]
        return cout

    def encrypt(self, message: str) -> str:
        message = list(message)
        first_key = [Six_directionAlgorithm.generate_sequence(self.seed, self.length)]
        second_key = [[],[],[],[],[]]
        morse_second_key = []
        TEXT_morse_second_key = ""
        for i in range(len(self.SECRET)):
            morse_second_key.append(__Mose__MAP__[self.SECRET[i]])

        # print(morse_second_key)
        for i in range(len(morse_second_key)):
            for j in range(len(morse_second_key[i])):
                TEXT_morse_second_key += str(morse_second_key[i][j])
                
        for i in range(len(TEXT_morse_second_key)):
            if i % 5 == 0:
                second_key[0].append(TEXT_morse_second_key[i])
            elif i % 5 == 1:
                second_key[1].append(TEXT_morse_second_key[i])
            elif i % 5 == 2:
                second_key[2].append(TEXT_morse_second_key[i])
            elif i % 5 == 3:
                second_key[3].append(TEXT_morse_second_key[i])
            elif i % 5 == 4:
                second_key[4].append(TEXT_morse_second_key[i])
        substitute = []
        for i in range(len(message)):
            # for j in range(len(first_key)):
                # print("sscc",first_key[j])
            substitute.append(Six_directionAlgorithm.how_to_go([message[i]],first_key[0],second_key[i]))
        cout = ""
        for i in range(len(substitute)):
            cout += substitute[i]
        return cout
    
    @staticmethod
    def de_how_to_go(Plaintext,first_key,second_key ) -> int:
        # print("first_key: ", first_key)
        # print("second_key: ", second_key)
        first = Six_directionAlgorithm.calculate_three(first_key)
        second = Six_directionAlgorithm.calculate_three(second_key)
        check = 0
        for i in range(len(second_key)):
            if i % 2 == 0:
                check += int(first_key[i]) * int(second_key[i])
            else:
                check -= int(second_key[i]) * int(first_key[i])

        # print("check: ", check,"first: ", first, "second: ", second)

        if first >= second:
            if check > 0:
                OPTION = 0
            elif check < 0:
                OPTION = 1
            else:
                OPTION = 2
        elif first < second:
            if check > 0:
                OPTION = 3
            elif check < 0:
                OPTION = 4
            else:
                OPTION = 5

        # return main(OPTION,Plaintext,abs(check))
        QQ = 0
        for i in range(len(first_key)):
            QQ += first_key[i]
        if i % 2 == 0:
            return Six_directionAlgorithm.de_main_tow(OPTION,Plaintext,abs(check))
        else :
            return Six_directionAlgorithm.de_main(OPTION,Plaintext,abs(check))
    
    @staticmethod
    def calculate_three(sequence):
        sum = 0
        for i in range(len(sequence)):
            sum += pow(5, len(sequence) - i - 1) * int(sequence[i])
        return sum
    
    @staticmethod
    def generate_sequence(seed, length):
        random.seed(seed)  # 設置隨機種子
        sequence = []
        for _ in range(length):
            choice = random.choice([0, 1, 2, 3])  # 從 [0, 1, 2, 3] 中隨機選擇一個數字
            sequence.append(choice)
        return sequence
    
    @staticmethod
    def how_to_go(Plaintext,first_key,second_key ) -> int:
        # print("first_key: ", first_key)
        # print("second_key: ", second_key)
        first = Six_directionAlgorithm.calculate_three(first_key)
        second = Six_directionAlgorithm.calculate_three(second_key)
        check = 0
        for i in range(len(second_key)):
            if i % 2 == 0:
                check += int(first_key[i]) * int(second_key[i])
            else:
                check -= int(second_key[i]) * int(first_key[i])

        # print("check: ", check,"first: ", first, "second: ", second)

        if first >= second:
            if check > 0:
                OPTION = 0
            elif check < 0:
                OPTION = 1
            else:
                OPTION = 2
        elif first < second:
            if check > 0:
                OPTION = 3
            elif check < 0:
                OPTION = 4
            else:
                OPTION = 5

        # return main(OPTION,Plaintext,abs(check))
        QQ = 0
        for i in range(len(first_key)):
            QQ += first_key[i]
        if i % 2 == 0:
            return Six_directionAlgorithm.main_tow(OPTION,Plaintext,abs(check))
        else :
            return Six_directionAlgorithm.main(OPTION,Plaintext,abs(check))
        
    @staticmethod
    def find_position(MAP, Plaintext):
        X_position = -1
        Y_position = -1

        for i in range(len(MAP)):
            for j in range(len(MAP[i])):
                if MAP[i][j] == Plaintext[0]:
                    X_position = i
                    Y_position = j
                    break
            if X_position != -1:
                break

        return X_position, Y_position
    
    @staticmethod
    def find_position_three_dimision(MAP, Plaintext):
        X_position = -1
        Y_position = -1
        Z_position = -1
        for i in range(len(__MAP__)):
            for j in range(len(__MAP__[i])):
                for z in range(len(__MAP__[i][j])):
                    if __MAP__[i][j][z] == Plaintext[0]:
                        X_position = j
                        Y_position = z
                        Z_position = i
                        break
                if X_position != -1:
                    break

        return X_position, Y_position,Z_position
    
    @staticmethod
    def main_tow(OPTION,Plaintext,check):
        X_position,Y_position,Z_position = Six_directionAlgorithm.find_position_three_dimision(__MAP__,Plaintext)
        # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", Plaintext, "check: ", check)
        # 前後左右上下
        if OPTION == 0:
            for i in range(check):
                if X_position + 1 == 4 or (X_position + 1 == 3 and Z_position == 3 and (Y_position == 2 or Y_position == 3)):
                    X_position = 0
                else:
                    X_position = X_position + 1
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
        elif OPTION == 1:
            for i in range(check):
                if X_position - 1 == -1:
                    if (Z_position == 3 and (Y_position == 2 or Y_position == 3)):
                        X_position = 2
                    else:
                        X_position = 3
                else:
                    X_position = X_position - 1
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
        elif OPTION == 2:
            for i in range(check):
                if Y_position - 1 == -1:
                    if (Z_position == 3 and X_position == 3):
                        Y_position = 1
                    else:
                        Y_position = 3
                else:
                    Y_position = Y_position - 1
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
        elif OPTION == 3:
            for i in range(check):
                if Y_position + 1 == 4 or (Y_position + 1 == 2 and Z_position == 3 and X_position == 3):
                    Y_position = 0
                else:
                    Y_position = Y_position + 1
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
                #"OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", 
        elif OPTION == 4:
            for i in range(check):
                if Z_position - 1 == -1:
                    if (X_position == 3 and (Y_position == 2 or Y_position == 3)):
                        Z_position = 2
                    else:
                        Z_position = 3
                else:
                    Z_position = Z_position - 1
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
        elif OPTION == 5:
            for i in range(check):
                if Z_position + 1 == 4 or (Z_position + 1 == 3 and X_position == 3 and (Y_position == 2 or Y_position == 3)):
                    Z_position = 0
                else:
                    Z_position = Z_position + 1
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
        return __MAP__[Z_position][X_position][Y_position]
    
    @staticmethod
    def main(OPTION,Plaintext,check) -> str:
        X_position, Y_position = Six_directionAlgorithm.find_position(MAP, Plaintext)
        # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", Plaintext, "check: ", check)
        if OPTION == 0:
            PATH = "右 上"
            step = 0
            # step = 0 右走
            # step = 1 上走
            for i in range(check):
                if step == 0:
                    if Y_position + 1 == len(MAP[X_position]):
                        Y_position = 0
                    else:
                        Y_position += 1
                    step = 1
                elif step == 1:
                    if X_position - 1 == -1:
                        if Y_position == 6 or Y_position == 7:
                            X_position = 6
                        else :
                            X_position = 7
                    else:
                        X_position -= 1
                    step = 0
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)

        elif OPTION == 1:
            PATH = "上 左"
            # step = 0 上走
            # step = 1 左走
            step = 0
            for i in range(check):
                if step == 0:
                    if X_position - 1 == -1:
                        if Y_position == 6 or Y_position == 7:
                            X_position = 6
                        else :
                            X_position = 7
                    else:
                        X_position -= 1
                    step = 1
                elif step == 1:
                    if Y_position - 1 == -1:
                        if X_position == 7:
                            Y_position = 5
                        else:
                            Y_position = len(MAP[X_position]) - 1
                    else:
                        Y_position -= 1
                    step = 0
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
        elif OPTION == 2:
            PATH = "X軸 下"
            # step = 0 下走
            # step = 1 右走

            for i in range(check):
                if Y_position + 1 == len(MAP[X_position]):
                    Y_position = 0
                    X_position += 1
                    if X_position == 8:
                        X_position = 0
                else:
                    Y_position += 1

                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
        elif OPTION == 3:
            PATH = "左 下"
            # step = 0 左走
            # step = 1 下走
            step = 0
            for i in range(check):
                if step == 0:
                    if Y_position - 1 == -1:
                        Y_position = len(MAP[X_position]) - 1
                    else:
                        Y_position -= 1
                    step = 1
                elif step == 1:
                    if X_position + 1 == 8 and (Y_position == 0 or Y_position == 1 or Y_position == 2 or Y_position == 3 or Y_position == 4 or Y_position == 5):
                        X_position = 0
                    elif X_position + 1 == 7 and (Y_position == 6 or Y_position == 7):
                        X_position = 0
                    else:
                        X_position += 1
                    step = 0
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
        elif OPTION == 4:
            PATH = "下 右"
            # step = 0 下走
            # step = 1 右走
            step = 0
            for i in range(check):
                if step == 0:
                    if X_position + 1 == 8 and (Y_position == 0 or Y_position == 1 or Y_position == 2 or Y_position == 3 or Y_position == 4 or Y_position == 5):
                        X_position = 0
                    elif X_position + 1 == 7 and (Y_position == 6 or Y_position == 7):
                        X_position = 0
                    else:
                        X_position += 1
                    step = 0
                elif step == 1:
                    if Y_position + 1 == len(MAP[X_position]):
                        X_position = 0
                    else:
                        X_position += 1
                    step = 0
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
        elif OPTION == 5:
            PATH = "Y軸 右"
            # step = 0 右走
            # step = 1 下走
            for i in range(check):
                if X_position + 1 == 8 and (Y_position == 0 or Y_position == 1 or Y_position == 2 or Y_position == 3 or Y_position == 4 or Y_position == 5):
                    X_position = 0
                    Y_position += 1
                elif X_position + 1 == 7 and (Y_position == 6 or Y_position == 7):
                    X_position = 0
                    Y_position += 1
                    if Y_position == 8:
                        Y_position = 0
                else:
                    X_position += 1
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
        # print(MAP[X_position][Y_position])
        return MAP[X_position][Y_position]
    
    @staticmethod
    def de_main_tow(OPTION,Plaintext,check):
        X_position,Y_position,Z_position = Six_directionAlgorithm.find_position_three_dimision(__MAP__,Plaintext)
        # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", Plaintext, "check: ", check)
        # 前後左右上下
        if OPTION == 1:
            for i in range(check):
                if X_position + 1 == 4 or (X_position + 1 == 3 and Z_position == 3 and (Y_position == 2 or Y_position == 3)):
                    X_position = 0
                else:
                    X_position = X_position + 1
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
        elif OPTION == 0:
            for i in range(check):
                if X_position - 1 == -1:
                    if (Z_position == 3 and (Y_position == 2 or Y_position == 3)):
                        X_position = 2
                    else:
                        X_position = 3
                else:
                    X_position = X_position - 1
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
        elif OPTION == 3:
            for i in range(check):
                if Y_position - 1 == -1:
                    if (Z_position == 3 and X_position == 3):
                        Y_position = 1
                    else:
                        Y_position = 3
                else:
                    Y_position = Y_position - 1
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
        elif OPTION == 2:
            for i in range(check):
                if Y_position + 1 == 4 or (Y_position + 1 == 2 and Z_position == 3 and X_position == 3):
                    Y_position = 0
                else:
                    Y_position = Y_position + 1
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
                #"OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", 
        elif OPTION == 5:
            for i in range(check):
                if Z_position - 1 == -1:
                    Z_position = 3
                else:
                    Z_position = Z_position - 1
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
        elif OPTION == 4:
            for i in range(check):
                if Z_position + 1 == 4 or (Z_position + 1 == 3 and X_position == 3 and (Y_position == 2 or Y_position == 3)):
                    Z_position = 0
                else:
                    Z_position = Z_position + 1
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
        return __MAP__[Z_position][X_position][Y_position]
    
    @staticmethod
    def de_main(OPTION,Plaintext,check) -> str:
        X_position, Y_position = Six_directionAlgorithm.find_position(MAP, Plaintext)
        # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", Plaintext, "check: ", check)
        if OPTION == 0:
            PATH = "右 上 => 下 左"
            step = 0
            # step = 0 右走
            # step = 1 上走
            if check % 2 == 1:
                step = 1
            for i in range(check):
                if step == 0:
                    if ((X_position + 1 == 7 and (Y_position == 6 or Y_position == 7)) or (X_position +1 == 8 and (Y_position == 0 or Y_position == 1 or Y_position == 2 or Y_position == 3 or Y_position == 4 or Y_position == 5))):
                        X_position = 0
                    else:
                        X_position += 1
                    step = 1
                elif step == 1:
                    if Y_position - 1 == -1:
                        if X_position == 7:
                            Y_position = 5
                        else :
                            Y_position = 7
                    else:
                        Y_position -= 1
                    step = 0
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)

        elif OPTION == 1:
            PATH = "上 左 => 右 下"
            # step = 0 上走
            # step = 1 左走
            step = 0
            if check %2 == 1:
                step = 1
            for i in range(check):
                if step == 0:
                    if Y_position + 1 == len(MAP[X_position]):
                        Y_position = 0
                    else:
                        Y_position += 1
                    step = 1
                elif step == 1:
                    if ((X_position + 1 == 7 and (Y_position == 6 or Y_position == 7)) or (X_position +1 == 8 and (Y_position == 0 or Y_position == 1 or Y_position == 2 or Y_position == 3 or Y_position == 4 or Y_position == 5))):
                        X_position = 0
                    else:
                        X_position += 1
                    step = 0
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
        elif OPTION == 2:
            PATH = "X軸 下"
            # step = 0 下走
            # step = 1 右走
            for i in range(check):
                if Y_position - 1 == -1:
                    if X_position == 0:
                        X_position = len(MAP)
                        Y_position = 5
                    else:
                        X_position -= 1 
                        Y_position = 7
                else:
                    Y_position -= 1

                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
        elif OPTION == 3:
            PATH = "左 下 => 上 右"
            # step = 0 左走
            # step = 1 下走
            step = 0
            if check %2 ==1:
                step = 1
            for i in range(check):
                if step == 0:
                    if X_position - 1 == -1:
                        if Y_position == 6 or Y_position == 7:
                            X_position = 6
                        else:
                            X_position = 7
                    else:
                        X_position -= 1
                    step = 1
                elif step == 1:
                    if Y_position + 1 == len(MAP[X_position]):
                        Y_position = 0
                    else:
                        Y_position += 1
                    step = 0
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
        elif OPTION == 4:
            PATH = "下 右 => 左 上"
            # step = 0 下走
            # step = 1 右走
            step = 0
            if check % 2 == 1:
                step = 1
            for i in range(check):
                if step == 0:
                    if Y_position - 1 == -1:
                        if X_position == 7:
                            Y_position = 5
                        else :
                            Y_position = 7
                    else:
                        Y_position -= 1
                    step = 0
                elif step == 1:
                    if X_position - 1 == -1:
                        if Y_position == 6 or Y_position == 7:
                            X_position = 6
                        else:
                            X_position = 7
                    else:
                        X_position -= 1
                    step = 0
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
        elif OPTION == 5:
            PATH = "Y軸 右"
            # step = 0 右走
            # step = 1 下走
            for i in range(check):
                if X_position - 1 == -1:
                    if Y_position == 0 or Y_position == 7:
                        X_position = 6
                        if X_position == 0:
                            X_position = 7
                        else:
                            X_position = 6
                    else:
                        X_position = 7
                        Y_position -= 1
                else:
                    X_position -= 1
                # print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
        # print(MAP[X_position][Y_position])
        return MAP[X_position][Y_position]