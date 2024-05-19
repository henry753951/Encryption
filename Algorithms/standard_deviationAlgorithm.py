from Map import MAP, __MAP__, __Mose__MAP__, __text__MAP__
from BaseEncryptAlgorithm import EncryptAlgorithm

import random
class standard_deviationAlgorithm(EncryptAlgorithm):
    def __init__(self, secret_key: str ) -> None:
        super().__init__(secret_key)
        self.seed = "1" + secret_key
        self.length = 5
        self.SECRET = secret_key

    def decrypt(self, secret: str) -> str:
        secret = list(secret)
        GG = standard_deviationAlgorithm.get_shift(secret)
        for i in range(len(secret)):
            now_shiht_left = (len(secret) + GG - i - 1) % len(secret)
            temp = secret[now_shiht_left]
            for j in range((now_shiht_left),0,-1):
                secret[j] = secret[j-1]
            secret[0]    = temp
        
        cout = ""
        for i in range(len(secret)):
            cout += secret[i]
        return cout

    def encrypt(self, message: str) -> str:
        GG = standard_deviationAlgorithm.get_shift(message)
        # encryption
        message = list(message)
        for i in range(len(message)):
            switch_temp = (i + GG) % len(message)
            __temp_text__ = message[0]
            if switch_temp == 0:
                # print(switch_temp,Plaintext)
                continue
            for j in range(switch_temp):
                message[j] = message[j+1]
            message[switch_temp] = __temp_text__
        cout = ""
        for i in range(len(message)):
           cout += message[i]
        return cout

    @staticmethod
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
