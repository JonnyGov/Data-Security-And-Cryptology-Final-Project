import Operations.DSA as DSA
import Helper
import Operations.OTPBacedOnVigenereCipher as OTPBacedOnVigenereCipher
import random

class Person:
     
    def __init__(self, shamirPart, p, q, g ,name):
         # p, q, g - parms for signuture
            self.shamirPart=shamirPart
            self.g=g
            self.p=p
            self.q=q
            self.x, self.y = DSA.generate_keys(self.g, self.p, self.q)
            self.name= name
        
        
    def encryptShamirPart(self):
        wordList=[]
        # shortWord=""
        # longerWrod=""
        for elm in self.shamirPart:
             wordList.append(Helper.numToWord(elm))
        
        # for elm in wordList:
        #     if len(elm)>len(longerWrod):
        #         longerWrod=elm
        #         else if: len(elm)<len(shorterWord):
        #         shorterWord =elm
        
        if self.shamirPart[0]>self.shamirPart[1]:
            randNum= random.sample(range((self.shamirPart[0]),(self.shamirPart[0])+ (self.shamirPart[1])), 1)
        else: 
            randNum= random.sample(range((self.shamirPart[1]),(self.shamirPart[0])+ (self.shamirPart[1])), 1)
            
        randNumAsWord=Helper.numToWord(randNum[0])
        ctext0=OTPBacedOnVigenereCipher.encrypt(wordList[0],randNumAsWord)
        ctext1=OTPBacedOnVigenereCipher.encrypt(wordList[1],randNumAsWord)
        
        return ctext0 ,ctext1,randNumAsWord
                
        
    def sign(self,word):
           M = str.encode(word, "ascii")
           r, s = DSA.sign(M, self.p, self.q, self.g, self.x)
           return r,s
       
    def fullEncryption(self):
            ctext0 ,ctext1,key =self.encryptShamirPart()
            r,s= self.sign(ctext0)
            ctext0RS=[r,s]
            r,s= self.sign(ctext1)
            ctext1RS=[r,s]
            return ctext0 ,ctext1,key,ctext0RS,ctext1RS
            
            
        
        
        