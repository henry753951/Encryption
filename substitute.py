from function import generate_sequence , how_to_go, de_how_to_go
__mose__MAP = {
    "A" : [0,0,0,1,2], "B" : [0,2,1,1,1], "C" : [0,2,1,2,1], "D" : [0,0,2,1,1], "E" : [0,0,0,0,1],
    "F" : [0,1,1,2,1], "G" : [0,0,2,2,1], "H" : [0,1,1,1,1], "I" : [0,0,0,1,1], "J" : [0,1,2,2,2],
    "K" : [0,0,2,1,2], "L" : [0,1,2,1,1], "M" : [0,0,0,2,2], "N" : [0,0,0,2,1], "O" : [0,0,2,2,2],
    "P" : [0,1,2,2,1], "Q" : [0,2,2,1,2], "R" : [0,0,1,2,1], "S" : [0,0,1,1,1], "T" : [0,0,0,0,2],
    "U" : [0,0,1,1,2], "V" : [0,0,1,1,2], "W" : [0,0,1,2,2], "X" : [0,2,1,1,2], "Y" : [0,2,1,2,2],
    "Z" : [0,2,2,1,1], "1" : [1,2,2,2,2], "2" : [1,1,2,2,2], "3" : [1,1,1,2,2], "4" : [1,1,1,1,2],
    "5" : [1,1,1,1,1], "6" : [2,1,1,1,1], "7" : [2,2,1,1,1], "8" : [2,2,2,1,1], "9" : [2,2,2,2,1],
    "0" : [2,2,2,2,2], "a" : [0,0,0,1,2], "b" : [0,2,1,1,1], "c" : [0,2,1,2,1], "d" : [0,0,2,1,1],
    "e" : [0,0,0,0,1], "f" : [0,1,1,2,1], "g" : [0,0,2,2,1], "h" : [0,1,1,1,1], "i" : [0,0,0,1,1],
    "j" : [0,1,2,2,2], "k" : [0,0,2,1,2], "l" : [0,1,2,1,1], "m" : [0,0,0,2,2], "n" : [0,0,0,2,1],
    "o" : [0,0,2,2,2], "p" : [0,1,2,2,1], "q" : [0,2,2,1,2], "r" : [0,0,1,2,1], "s" : [0,0,1,1,1],
    "t" : [0,0,0,0,2], "u" : [0,0,1,1,2], "v" : [0,1,1,1,2], "w" : [0,0,1,2,2], "x" : [0,2,1,1,2],
    "y" : [0,2,1,2,2], "z" : [0,2,2,1,1],}

seed = "267814"  # 固定種子
length = 5  # 生成序列的長度

first_key = [generate_sequence(seed, length)]
second_key = [[],[],[],[],[]]
secret_key = "67814"
Plaintext = list(input("Enter the Plaintext: "))
# print("Plaintext: ", first_key)
# 1 [1, 2, 0, 1, 0]
# 2 [1, 2, 1, 1, 3]
# 3 [0, 3, 3, 2, 2]
# 4 [0, 3, 2, 2, 3]
# 5 [0, 2, 1, 3, 1]
# 6 [0, 3, 0, 3, 3]

morse_second_key = []
TEXT_morse_second_key = ""
for i in range(len(secret_key)):
    morse_second_key.append(__mose__MAP[secret_key[i]])
    
# print(morse_second_key)
for i in range(len(morse_second_key)):
    for j in range(len(morse_second_key[i])):
        TEXT_morse_second_key += str(morse_second_key[i][j])
        
# 間隔抓key 例如[[0, 0, 2, 2, 1], [0, 0, 0, 0, 2], [0, 0, 1, 2, 1]]  -> [[0, 0, 0], [0, 0, 0], [2, 0, 1], [2, 0, 2], [1, 2, 1]]
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
for i in range(len(Plaintext)):
    # for j in range(len(first_key)):
        # print("sscc",first_key[j])
    substitute.append(how_to_go([Plaintext[i]],first_key[0],second_key[i]))
print("加密後 : ",substitute)

#//////////////////////////////
encript = ""
for i in range(len(substitute)):
    encript += substitute[i]
# 開始解密
print("開始解密")
de_first_key = [generate_sequence(seed, length)]
de_second_key = [[],[],[],[],[]]

de_morse_second_key = []
de_TEXT_morse_second_key = ""
for i in range(len(secret_key)):
    de_morse_second_key.append(__mose__MAP[secret_key[i]])
    
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
for i in range(len(encript)):
    # for j in range(len(first_key)):
        # print("sscc",first_key[j])
    de_substitute.append(de_how_to_go([encript[i]],de_first_key[0],de_second_key[i]))
print("解密回來後 : ",de_substitute)