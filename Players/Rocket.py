
import Operations.DSA as DSA
import Helper
import Operations.OTPBacedOnVigenereCipher as OTPBacedOnVigenereCipher
import random
import Operations.shamir as shamir
import Player as P
class Rocket(P.Player):
    shamirParts=[]
    def __init__(self, Shamirsecret, p, q, g ,name,otpDic):
             # p, q, g - parms for signuture
            self.Shamirsecret=Shamirsecret
            super().__init__(name, p, q, g,otpDic) 
            
    def reciveShamirKeyPart(self,dealerShamirKeyPart):
        if(not super().IdUser(name,dealerShamirKeyPart[1],dealerShamirKeyPart[2],dealerShamirKeyPart[3])):
            return False
        #taking the shamir thingi and adding it to the shmir part list 
        shamirPart=[]
        temp=self.getShamirPart(ctext0,key)
        shamirPart.append(temp)
        shamirPart.append(self.getShamirPart(ctext1,key))
        self.shamirParts.append(shamirPart)
        return True
        
        
    def getShamirPart(self,ctext,key):
         ptext=OTPBacedOnVigenereCipher.decrypt(ctext,key)
         return Helper.wordToNum(ptext)
         
    def reconstructAndTestSecret(self):
          #print(self.shamirParts)
         return  shamir.reconstructSecret(self.shamirParts) ==self.Shamirsecret
        
        
    
    
        