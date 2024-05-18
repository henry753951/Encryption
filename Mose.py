__text__MAP__ = {
    "A" : 1, "B" : 2, "C" : 3, "D" : 4, "E" : 5, 
    "F" : 6, "G" : 7, "H" : 8, "I" : 9, "J" : 10, 
    "K" : 11, "L" : 12, "M" : 13, "N" : 14, "O" : 15, 
    "P" : 16, "Q" : 17, "R" : 18, "S" : 19, "T" : 20, 
    "U" : 21, "V" : 22, "W" : 23, "X" : 24, "Y" : 25, 
    "Z" : 26, "1" : 27, "2" : 28, "3" : 29, "4" : 30,
    "5" : 31, "6" : 32, "7" : 33, "8" : 34, "9" : 35,
    "0" : 36, "a" : 37, "b" : 38, "c" : 39, "d" : 40,
    "e" : 41, "f" : 42, "g" : 43, "h" : 44, "i" : 45,
    "j" : 46, "k" : 47, "l" : 48, "m" : 49, "n" : 50,
    "o" : 51, "p" : 52, "q" : 53, "r" : 54, "s" : 55,
    "t" : 56, "u" : 57, "v" : 58, "w" : 59, "x" : 60,
    "y" : 61, "z" : 62,}
def get_shift(Plaintext: str):
    shift = 0
    average = 0
    for i in range(len(Plaintext)):
        average += __text__MAP__[Plaintext[i]]
    average = average/len(Plaintext)
    for i in range(len(Plaintext)):
        shift += round(pow((__text__MAP__[Plaintext[i]] - average),2),0)
    shift = round(pow(shift/len(Plaintext),0.5))
    return shift

Plaintext = list(input("Enter the Plaintext: "))
GG = get_shift(Plaintext)
print(GG)
new_text = [''] * len(Plaintext)

# encryption
for i in range(len(Plaintext)):
    switch_temp = (i + GG) % len(Plaintext)
    __temp_text__ = Plaintext[0]
    if switch_temp == 0:
        # print(switch_temp,Plaintext)
        continue
    for j in range(switch_temp):
        Plaintext[j] = Plaintext[j+1]
    Plaintext[switch_temp] = __temp_text__
    # print(switch_temp,Plaintext)
print("Plaintext: ",Plaintext)


FINALLY = []
# decryption
for i in range(len(Plaintext)):
    now_shiht_left = (len(Plaintext) + GG - i - 1) % len(Plaintext)
    temp = Plaintext[now_shiht_left]
    for j in range((now_shiht_left),0,-1):
        Plaintext[j] = Plaintext[j-1]
    Plaintext[0]    = temp
    print(Plaintext)