
import Operations.DSA as DSA
import Helper
import Operations.OTPBacedOnVigenereCipher as OTPBacedOnVigenereCipher
import random
import Operations.shamir as shamir

class Rocket:
    publickeys={}
    shamirParts=[]
    def __init__(self, Shamirsecret, p, q, g ,name):
             # p, q, g - parms for signuture
            self.Shamirsecret=Shamirsecret
            self.g=g
            self.p=p
            self.q=q
            self.x, self.y = DSA.generate_keys(self.g, self.p, self.q)
            self.name= name
            
    def receivePublicKey(self, key,name):
        self.publickeys[name]=key
        
        
    def reciveShamirKeyPart(self,senderName,ctext0 ,ctext1,key,ctext0RS,ctext1RS):
        
         if(senderName in self.publickeys):
              senderNameKey=self.publickeys[senderName]
         else: return False 
         
         
         if DSA.verify(str.encode(ctext0, "ascii"), ctext0RS[0], ctext0RS[1], self.p, self.q, self.g, senderNameKey):
            print('All ok')
         else:
            print('not ok')
            return False 
        
         if DSA.verify(str.encode(ctext1, "ascii"), ctext1RS[0], ctext1RS[1], self.p, self.q, self.g, senderNameKey):
            print('All ok')
         else:
            print('not ok')
            return False 
         shamirPart=[]
         temp=self.getShamirPart(ctext0,key)
         shamirPart.append(temp)
         shamirPart.append(self.getShamirPart(ctext1,key))
         self.shamirParts.append(shamirPart)
         return True
        
        
    def getShamirPart(self,ctext,key):
         ptext=OTPBacedOnVigenereCipher.decrypt(ctext,key)
         return Helper.wordToNum(ptext)
         
    def reconstructSecret(self):
         return shamir.reconstructSecret(self.shamirParts)
        
        
    
    
        