import random
MAP = [
    ["A", "B", "C", "D", "E", "F", "G", "H"],
    ["I", "J", "K", "L", "M", "N", "O", "P"],
    ["Q", "R", "S", "T", "U", "V", "W", "X"],
    ["Y", "Z", "1", "2", "3", "4", "5", "6"],
    ["7", "8", "9", "0", "a", "b", "c", "d"],
    ["e", "f", "g", "h", "i", "j", "k", "l"],
    ["m", "n", "o", "p", "q", "r", "s", "t"],
    ["u", "v", "w", "x", "y", "z"] 
]

__MAP__ = [[["A", "B", "C", "D"],["E", "F", "G", "H"],["I", "J", "K", "L"],["M", "N", "O", "P"]],
           [["Q", "R", "S", "T"],["U", "V", "W", "X"],["Y", "Z", "1", "2"],["3", "4", "5", "6"]],
           [["7", "8", "9", "0"],["a", "b", "c", "d"],["e", "f", "g", "h"],["i", "j", "k", "l"]],
           [["m", "n", "o", "p"],["q", "r", "s", "t"],["u", "v", "w", "x"],["y", "z"]]           
           ]
def generate_sequence(seed, length):
    random.seed(seed)  # 設置隨機種子
    sequence = []
    for _ in range(length):
        choice = random.choice([0, 1, 2, 3])  # 從 [0, 1, 2, 3] 中隨機選擇一個數字
        sequence.append(choice)
    return sequence

# !!!!!!!!!!!!想遺下要用幾近衛!!!!!!!!!!!!
def calculate_three(sequence):
    sum = 0
    for i in range(len(sequence)):
        sum += pow(5, len(sequence) - i - 1) * int(sequence[i])
    return sum

# Plaintext:  ['r']
# First Key:  [1, 2, 0, 1, 0]
# Second Key:  ['1', '1', '2', '2', '1']

# 0 K1 大於等於 K2 calculate > 0
# 1 K1 大於等於 K2 calculate < 0
# 2 K1 大於等於 K2 calculate = 0
# 3 K1 小於 K2 calculate > 0
# 4 K1 小於 K2 calculate < 0
# 5 K1 小於 K2 calculate = 0

def how_to_go(Plaintext,first_key,second_key ) -> int:
    print("first_key: ", first_key)
    print("second_key: ", second_key)
    first = calculate_three(first_key)
    second = calculate_three(second_key)
    check = 0
    for i in range(len(second_key)):
        if i % 2 == 0:
            check += int(first_key[i]) * int(second_key[i])
        else:
            check -= int(second_key[i]) * int(first_key[i])
        
    print("check: ", check,"first: ", first, "second: ", second)

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
        return main_tow(OPTION,Plaintext,abs(check))
    else :
        return main(OPTION,Plaintext,abs(check))


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
#//////////////////

def main_tow(OPTION,Plaintext,check):
    X_position,Y_position,Z_position = find_position_three_dimision(__MAP__,Plaintext)
    print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", Plaintext, "check: ", check)
    # 前後左右上下
    if OPTION == 0:
        for i in range(check):
            if X_position + 1 == 4 or (X_position + 1 == 3 and Z_position == 3 and (Y_position == 2 or Y_position == 3)):
                X_position = 0
            else:
                X_position = X_position + 1
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
    elif OPTION == 1:
        for i in range(check):
            if X_position - 1 == -1:
                if (Z_position == 3 and (Y_position == 2 or Y_position == 3)):
                    X_position = 2
                else:
                    X_position = 3
            else:
                X_position = X_position - 1
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
    elif OPTION == 2:
        for i in range(check):
            if Y_position - 1 == -1:
                if (Z_position == 3 and X_position == 3):
                    Y_position = 1
                else:
                    Y_position = 3
            else:
                Y_position = Y_position - 1
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
    elif OPTION == 3:
        for i in range(check):
            if Y_position + 1 == 4 or (Y_position + 1 == 2 and Z_position == 3 and X_position == 3):
                Y_position = 0
            else:
                Y_position = Y_position + 1
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
            #"OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", 
    elif OPTION == 4:
        for i in range(check):
            if Z_position - 1 == -1:
                Z_position = 3
            else:
                Z_position = Z_position - 1
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
    elif OPTION == 5:
        for i in range(check):
            if Z_position + 1 == 4 or (Z_position + 1 == 3 and X_position == 3 and (Y_position == 2 or Y_position == 3)):
                Z_position = 0
            else:
                Z_position = Z_position + 1
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
    return __MAP__[Z_position][X_position][Y_position]
#//////////////////

def main(OPTION,Plaintext,check) -> str:
    X_position, Y_position = find_position(MAP, Plaintext)
    print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", Plaintext, "check: ", check)
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
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
            
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
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
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

            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
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
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
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
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
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
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
    print(MAP[X_position][Y_position])
    return MAP[X_position][Y_position]


#!!!!!!!!!!!!!!解密!!!!!!!!!!!!!!

def de_how_to_go(Plaintext,first_key,second_key ) -> int:
    print("first_key: ", first_key)
    print("second_key: ", second_key)
    first = calculate_three(first_key)
    second = calculate_three(second_key)
    check = 0
    for i in range(len(second_key)):
        if i % 2 == 0:
            check += int(first_key[i]) * int(second_key[i])
        else:
            check -= int(second_key[i]) * int(first_key[i])
        
    print("check: ", check,"first: ", first, "second: ", second)

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
        return de_main_tow(OPTION,Plaintext,abs(check))
    else :
        return de_main(OPTION,Plaintext,abs(check))


def de_main_tow(OPTION,Plaintext,check):
    X_position,Y_position,Z_position = find_position_three_dimision(__MAP__,Plaintext)
    print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", Plaintext, "check: ", check)
    # 前後左右上下
    if OPTION == 1:
        for i in range(check):
            if X_position + 1 == 4 or (X_position + 1 == 3 and Z_position == 3 and (Y_position == 2 or Y_position == 3)):
                X_position = 0
            else:
                X_position = X_position + 1
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
    elif OPTION == 0:
        for i in range(check):
            if X_position - 1 == -1:
                if (Z_position == 3 and (Y_position == 2 or Y_position == 3)):
                    X_position = 2
                else:
                    X_position = 3
            else:
                X_position = X_position - 1
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
    elif OPTION == 3:
        for i in range(check):
            if Y_position - 1 == -1:
                if (Z_position == 3 and X_position == 3):
                    Y_position = 1
                else:
                    Y_position = 3
            else:
                Y_position = Y_position - 1
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
    elif OPTION == 2:
        for i in range(check):
            if Y_position + 1 == 4 or (Y_position + 1 == 2 and Z_position == 3 and X_position == 3):
                Y_position = 0
            else:
                Y_position = Y_position + 1
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
            #"OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", 
    elif OPTION == 5:
        for i in range(check):
            if Z_position - 1 == -1:
                Z_position = 3
            else:
                Z_position = Z_position - 1
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
    elif OPTION == 4:
        for i in range(check):
            if Z_position + 1 == 4 or (Z_position + 1 == 3 and X_position == 3 and (Y_position == 2 or Y_position == 3)):
                Z_position = 0
            else:
                Z_position = Z_position + 1
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Z_position: ", Z_position, "Plaintext: ", __MAP__[Z_position][X_position][Y_position], "check: ", check)
    return __MAP__[Z_position][X_position][Y_position]

def de_main(OPTION,Plaintext,check) -> str:
    X_position, Y_position = find_position(MAP, Plaintext)
    print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", Plaintext, "check: ", check)
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
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
            
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
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
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

            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
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
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
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
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
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
            print("OPTION: ", OPTION,"X_position: ", X_position, "Y_position: ", Y_position, "Plaintext: ", MAP[X_position][Y_position], "check: ", check)
    print(MAP[X_position][Y_position])
    return MAP[X_position][Y_position]