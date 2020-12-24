import Operations.DSA as DSA
import random 
import Helper
import Operations.OTPBacedOnVigenereCipher as OTPBacedOnVigenereCipher
class Player:
     publicSignaturekeys={}
              
     def __init__(self,name ,p, q, g):
         self.name=name
         #params for DSA
         self.g=g
         self.p=p
         self.q=q
         
     def receiveSignaturePublicKey(self, key,name):
        self.publicSignaturekeys[name]=key
        
     def testIfHasSignarurePublicKey(self,senderName):
         if(senderName in self.publicSignaturekeys):
                  senderKey=self.publicSignaturekeys[senderName]
                  return senderKey
         else:
                  print( self.name +": unknown sender not approved")
                  return False 
              
     def IdUser(self,name,Mstring,r,s):
         publicKey =self.testIfHasSignarurePublicKey(name)
         if(publicKey == False):
             return False
         M= str.encode(Mstring, "ascii")
         if DSA.verify(M, r, s, self.p, self.q, self.g, publicKey):
             print(self.name +": "+ name+ " is approved")
             return True
         
             
     def encryptInt(self,number):
          
        randForMult=random.sample(range(0,int(number/2)), 1)                      
        randNum= random.sample(range(number,abs(number + randForMult[0])), 1)      
        randNumAsWord=Helper.numToWord(randNum[0])
        word=Helper.numToWord(number)
        ctext=OTPBacedOnVigenereCipher.encrypt(word ,randNumAsWord)
        return ctext ,randNumAsWord  
    
     def encryptString(self,word):
        number = Helper.wordToNum(word)
        randForMult=random.sample(range(0,int(number/2)), 1)                  
        randNum= random.sample(range(number, abs(number + randForMult[0])), 1)
        randNumAsWord=Helper.numToWord(randNum[0])
        ctext=OTPBacedOnVigenereCipher.encrypt(word ,randNumAsWord)
        return ctext ,randNumAsWord  
    
    
     def  decryptAsNum(self,ctext,key):
         ptext=OTPBacedOnVigenereCipher.decrypt(ctext,key)
         return Helper.wordToNum(ptext)
     
     def  decryptAsString(self,ctext,key):
         ptext=OTPBacedOnVigenereCipher.decrypt(ctext,key)
         return ptext
     
 #------------------------------------testing ------------------------------------------------------------------------------------------------------------
def testingOTP():
   player =Player("someting", 1, 1, 1)
   ctext ,key=  player.encryptInt(45)
   text=player.decryptAsNum( ctext ,key)
   print(text)
   
   ctext ,key=  player.encryptString("planetext")
   text=player.decryptAsString( ctext ,key)
   print(text)
    
       
if __name__ == '__main__': 
  testingOTP()