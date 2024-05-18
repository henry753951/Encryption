# from abc import ABC, abstractmethod
from BaseEncryptAlgorithm import EncryptAlgorithm

# class EncryptAlgorithm(ABC):
#     secret_key = None
#     def __init__(self, secret_key: str):
#         self.secret_key = secret_key
    
#     @abstractmethod
#     def encrypt(self, message: str) -> str:
#         pass
#     @abstractmethod
#     def decrypt(self, secret: str) -> str:
#         pass
    
class EZICEncryptAlgorithm(EncryptAlgorithm):
    key_table = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    text_max = len(key_table)
    
    def __init__(self, secret_key: str):
        super().__init__(secret_key)        
        
    def encrypt(self, message: str) -> str:
        tempKey = self.changeKeyLength(self.secret_key,message)
        key_in_number = [self.key_table.index(i) for i in tempKey]
        
        message_in_number = [self.key_table.index(i) for i in message]
        map1 = [list(range(self.text_max)) for _ in range(len(message))] #step1 建立map1
        self.shiftMap(map1,key_in_number) #step2 改變map1 : 將map1的每一行向右shift key[i]個位置
        location = self.findLocation(message_in_number,key_in_number) #step3 找出mask孔洞 : 找出每個text_input對應到key_table的index
        
        up = key_in_number[0]+key_in_number[2] #往上shift的量是key[0]+key[2]+key[4]
        right = key_in_number[1]+key_in_number[3] #往右shift的量是key[1]+key[3]
        if up >= self.text_max:
            up = up - self.text_max
        if right >= self.text_max:
            right = right - self.text_max
            
        shiftedLocation = self.shiftLocation(location,up,right) #step4 mask孔洞位移 : 將location的每一行向上shift up個位置，向右shift right個位置
        encypted_code = self.location2code(map1,shiftedLocation) #step5 找出加密後的文字 : 將location的每一行的index轉換成map1的值
        encypted_code_in_text = ''.join([self.key_table[i] for i in encypted_code])
        encrypted_message = encypted_code_in_text
        return encrypted_message

    def decrypt(self, secret: str) -> str:
        tempKey = self.changeKeyLength(self.secret_key,secret)
        key_in_number = [self.key_table.index(i) for i in tempKey]
        
        secret_in_number = [self.key_table.index(i) for i in secret] 
        map1 = [list(range(self.text_max)) for _ in range(len(secret))] #step1 建立map1
        self.shiftMap(map1,key_in_number) #step2 改變map1 : 將map1的每一行向右shift key[i]個位置
        locationR = self.findLocation(secret_in_number,key_in_number) #step3 找出mask孔洞 : 找出每個text_input對應到key_table的index
        
        down = key_in_number[0]+key_in_number[2] #往下shift的量是key[0]+key[2]+key[4]
        left = key_in_number[1]+key_in_number[3] #往左shift的量是key[1]+key[3]
        if down >= self.text_max:
            down = down - self.text_max
        if left >= self.text_max:
            left = left - self.text_max
        down = -down #往下shift的量是負的
        left = -left #往左shift的量是負的
        shiftedBackLocation = self.shiftLocation(locationR,down,left) #step4 mask孔洞位移 : 將location的每一行向下shift down個位置，向左shift left個位置
        reMessage = self.findMessage(shiftedBackLocation,key_in_number) #step5 找出解密後的文字 : 將location的每一行的index轉換成map1的值
        reMessage_in_text = ''.join([self.key_table[i] for i in reMessage])
        
        decrypted_message = reMessage_in_text
        return decrypted_message
    
    def changeKeyLength(self,key,message): #將key的長度改為與message相同
        if len(key) < len(message):
            key = key*(len(message)//len(key)) + key[:len(message)%len(key)]
        elif len(key) > len(message):
            key = key[:len(message)]
        return key
    
    def shiftMap(self,map1,key): #將map1的每一行向右shift key[i]個位置
        for i in range(len(key)):
            last_elements = map1[i][-key[i]:]
            map1[i] = last_elements + map1[i][:-key[i]]
    
    def findLocation(self,message,key): #找出每個text_input對應到key_table的index
        ans = []
        for i in range(len(message)):
            temp = message[i]+key[i] #原本的位置加上key(該行shift量)=新的位置
            if temp >= self.text_max:
                temp = temp - self.text_max
            ans.append(temp)
        return ans

    def findMessage(self,location,key): #找回原本的text_input對應到key_table的index
        ans = []
        for i in range(len(location)):
            temp = location[i]-key[i] #現在的位置減去key(該行-shift量)=原本的位置
            if temp < 0:
                temp = temp + self.text_max
            ans.append(temp)
        return ans

    def shiftLocation(self,location,up,right): #將location的每一行向上shift up個位置，向右shift right個位置
        ans = []
        for i in location:
            temp = i + right
            if temp >= self.text_max:
                temp = temp - self.text_max
            ans.append(temp)
        tempUp = up % len(location)
        front_elements = ans[tempUp:]
        ans = front_elements + ans[:tempUp]
            
        return ans

    def location2code(self,map1,location): #將location的每一行的index轉換成map1的值
        ans = []
        for i in range(len(location)):
            ans.append(map1[i][location[i]])
        return ans

# main-----------------------------------------------------------------------------------------

# TheMessage = "PIYAN"
# TheKEY = "PIYAN"
# if len(TheMessage) != len(TheKEY):
#     print("The length of the key must be equal to the length of the message")
#     exit()
# print("Original Message:", TheMessage)
# print("KEY:", TheKEY)

# EZICencrypt = EZICEncryptAlgorithm(TheKEY)

# encrypted_text = EZICencrypt.encrypt(TheMessage)
# print("Encrypted:", encrypted_text)

# decrypted_text = EZICencrypt.decrypt(encrypted_text)
# print("Decrypted:", decrypted_text)

# main end-------------------------------------------------------------------------------------

# key_table = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
# text_max = len(key_table)
# message_in_text = 'PIYAN'
# print("原始",message_in_text)
# key_in_text = 'PIYAN'
# #message為text_input對應到key_table的index
# message = [key_table.index(i) for i in message_in_text]
# key = [key_table.index(i) for i in key_in_text]

# def shiftMap(map1,key): #將map1的每一行向右shift key[i]個位置
#     for i in range(len(message)):
#         last_elements = map1[i][-key[i]:]
#         map1[i] = last_elements + map1[i][:-key[i]]
    
# def findLocation(message,key): #找出每個text_input對應到key_table的index
#     ans = []
#     for i in range(len(message)):
#         temp = message[i]+key[i] #原本的位置加上key(該行shift量)=新的位置
#         if temp >= text_max:
#             temp = temp - text_max
#         ans.append(temp)
#     return ans

# def findMessage(location,key): #找回原本的text_input對應到key_table的index
#     ans = []
#     for i in range(len(location)):
#         temp = location[i]-key[i] #現在的位置減去key(該行-shift量)=原本的位置
#         if temp < 0:
#             temp = temp + text_max
#         ans.append(temp)
#     return ans

# def shiftLocation(location,up,right): #將location的每一行向上shift up個位置，向右shift right個位置
#     ans = []
#     for i in location:
#         temp = i + right
#         if temp >= text_max:
#             temp = temp - text_max
#         ans.append(temp)
#     tempUp = up % len(location)
#     front_elements = ans[tempUp:]
#     ans = front_elements + ans[:tempUp]
        
#     return ans

# def location2code(map1,location): #將location的每一行的index轉換成map1的值
#     ans = []
#     for i in range(len(location)):
#         ans.append(map1[i][location[i]])
#     return ans

# # step1 建立map1
# map1 = [list(range(text_max)) for _ in range(text_max)]

# # step2 將map1的每一行向右shift key[i]個位置
# shiftMap(map1,key)
# # print(map1)

# # step3 找出每個text_input對應到key_table的index
# location = findLocation(message,key)
# # print(location)

# # step4 將location的每一行向上shift up個位置，向右shift right個位置
# up = key[0]+key[2]+key[4]
# right = key[1]+key[3]
# if up >= text_max:
#     up = up - text_max
# if right >= text_max:
#     right = right - text_max

# shiftedLocation = shiftLocation(location,up,right)
# # print(shiftedLocation)

# # step5 將location的每一行的index轉換成map1的值
# encypted_code = location2code(map1,shiftedLocation)
# # print(encypted_code)
# encypted_code_in_text = ''.join([key_table[i] for i in encypted_code])
# print("加密",encypted_code_in_text)

# decryption.................................................................................

# # step1 建立map1
# map1 = [list(range(text_max)) for _ in range(text_max)]

# # step2 將map1的每一行向右shift key[i]個位置
# shiftMap(map1,key)

# # step3 找出每個text_input對應到key_table的index
# locationR = findLocation(encypted_code,key)

# # step4 將location的每一行向下shift down個位置，向左shift left個位置
# down = key[0]+key[2]+key[4]
# left = key[1]+key[3]
# if down >= text_max:
#     down = down - text_max
# if left >= text_max:
#     left = left - text_max
# down = -down
# left = -left

# shiftedBackLocation = shiftLocation(locationR,down,left)

# # step5 將location的每一行的index轉換成map1的值
# reMessage = findMessage(shiftedBackLocation,key)
# reMessage_in_text = ''.join([key_table[i] for i in reMessage])
# print("解密",reMessage_in_text)