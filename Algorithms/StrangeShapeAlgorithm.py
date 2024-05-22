import random
import math
from BaseEncryptAlgorithm import EncryptAlgorithm


class StrangeShapeAlgorithm(EncryptAlgorithm):
    def __init__(self, secret_key: str) -> None:
        super().__init__(secret_key)
        self.ShapeMap = None
        self.key=secret_key
    
    def print_map(self,map): #印出地圖和有字母的數量
        count=0
        for row in map:
            for element in row:
                if element != '*':
                    count += 1
                print(element, end=" ")
            print("\n")
        print("----------------------------------------------------------------------"+str(count))
        return count
    def NumberOfMember(self,map):#單純取得地圖字母的數量
        count=0
        for row in map:
            for element in row:
                if element != '*':
                    count += 1
        return count    

    def generate_Map(self, length):
        random.seed(self.key)  # 設置隨機種子
        sizes=length*2+3 #保證地圖大小足夠
        myMap=[['*' for col in range(sizes)] for row in range(sizes)]
        #self.print_map(myMap)
        
        col=new_col=length+1
        row=new_row=length+1
        
        #對Map進行遍歷，並對每個元素看要不要往外增長
        while(self.NumberOfMember(myMap)<length):
            road=["up", "down", "right", "left"]
            row=new_row
            col=new_col
            myMap[row][col] = '&'
            #self.print_map(myMap)
            for i in range(4):
                choice = random.choice(road)
                road.remove(choice)
                #print(choice)
                try:
                    Count= self.NumberOfMember(myMap)
                    if Count >= length:
                        break 
                    if choice == "up":
                        if myMap[row-1][col] != '*':
                            continue
                        myMap[row-1][col] = '&'
                        new_col=col
                        new_row=row-1
                except:
                    pass
                try:
                    Count= self.NumberOfMember(myMap)
                    if Count >= length:
                        break 
                    if choice == "up":
                        if myMap[row+1][col] != '*':
                            continue
                        myMap[row+1][col] = '&'
                        new_col=col
                        new_row=row+1
                except:
                    pass   
                try:
                    Count= self.NumberOfMember(myMap)
                    if Count >= length:
                        break 
                    if choice == "right":
                        if myMap[row][col+1] != '*':
                            continue
                        myMap[row][col+1] = '&'
                        new_col=col+1
                        new_row=row
                except:
                    pass   
                try:
                    Count= self.NumberOfMember(myMap)
                    if Count >= length:
                        break 
                    if choice == "left":
                        if myMap[row][col-1] != '*':
                            continue
                        myMap[row][col-1] = '&'
                        new_col=col-1
                        new_row=row
                except:
                    pass
            
        #self.print_map(myMap)
        return myMap
    
    def PutTextEn(self, Nowmap, text):
        index=0
        for col_index in range(len(Nowmap[0])):
            for row in Nowmap:
                if index > len(text):
                    break
                if row[col_index] == '&':
                    row[col_index]=text[index]
                    index+=1
        return Nowmap
    def PutTextDe(self, Nowmap, text):
        index=0
        for row in Nowmap:
            for col_index in range(len(Nowmap[0])):
                if index > len(text):
                    break
                if row[col_index] == '&':
                    row[col_index]=text[index]
                    index+=1
        
        return Nowmap
    
    def encrypt(self, text):
        ENmap= self.generate_Map(len(text))
        ciphertext=""
        index=0
        ENmap = self.PutTextEn(ENmap,text)
        #self.print_map(ENmap)
        for row in ENmap:
            for element in row:
                if element != '*':
                    ciphertext += element
        #print(ciphertext)
        return ciphertext
                    

    def decrypt(self, encrypted_text):
        DEmap= self.generate_Map(len(encrypted_text))
        plaintext= ""
        DEmap = self.PutTextDe(DEmap,encrypted_text)
        #self.print_map(DEmap)
        for col_index in range(len(DEmap[0])):
            for row in DEmap:
                if row[col_index] != '*':
                    plaintext += row[col_index]
        #print(plaintext)
        return plaintext
