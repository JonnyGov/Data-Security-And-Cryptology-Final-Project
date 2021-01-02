import Operations.DSA as DSA
import random 
import Helper
import Operations.OTPBacedOnVigenereCipher as OTPBacedOnVigenereCipher
from deprecated import deprecated
import  sys
import math

class Player:
     publicSignaturekeys={}
              
     def __init__(self,name ,p, q, g,otpDic):
         self.name=name
         #params for DSA
         self.g=g
         self.p=p
         self.q=q
         self.__otpDic=otpDic
         self.__x, self.y = DSA.generate_keys(self.g, self.p, self.q)
         
     def receiveSignaturePublicKey(self, key,name):
        self.publicSignaturekeys[name]=key
        
     def testIfHasSignarurePublicKey(self,senderName):
         if(senderName in self.publicSignaturekeys):
                  senderKey=self.publicSignaturekeys[senderName]
                  return senderKey
         else:
                  print( self.name +": unknown sender not approved")
                  return False 
              
     # verify dsa signature.        
     def IdUser(self,name,Mstring,r,s):
         publicKey =self.testIfHasSignarurePublicKey(name)
         if(publicKey == False):
             return False
         M= str.encode(Mstring, "ascii")
         if DSA.verify(M, r, s, self.p, self.q, self.g, publicKey):
             print(self.name +": "+ name+ " is approved")
             return True
         else:
             print(self.name +": "+ name+ " is NOT approved")
         
     @deprecated( reason="You should use encryptStringOTP") 
     def encryptInt(self,number):          
        randForMult=random.sample(range(0,int(number/2)), 1)                      
        randNum= random.sample(range(number,abs(number + randForMult[0])), 1)      
        randNumAsWord=Helper.numToWord(randNum[0])
        word=Helper.numToWord(number)
        ctext=OTPBacedOnVigenereCipher.encrypt(word ,randNumAsWord)
        return ctext ,randNumAsWord  
     @deprecated( reason="You should use encryptStringOTP") 
     def encryptString(self,word):
        number = Helper.wordToNum(word)
        randForMult=random.sample(range(0,int(number/2)), 1)                  
        randNum= random.sample(range(number, abs(number + randForMult[0])), 1)
        randNumAsWord=Helper.numToWord(randNum[0])
        ctext=OTPBacedOnVigenereCipher.encrypt(word ,randNumAsWord)
        return ctext ,randNumAsWord  
    
     @deprecated( reason="You should use decryptAsStringOTP") 
     def  decryptAsNum(self,ctext,key):
         ptext=OTPBacedOnVigenereCipher.decrypt(ctext,key)
         return Helper.wordToNum(ptext)
     
        
     @deprecated( reason="You should use decryptAsStringOTP") 
     def  decryptAsString(self,ctext,key):
         ptext=OTPBacedOnVigenereCipher.decrypt(ctext,key)
         return ptext
     
     def sign(self,word):
           M = str.encode(word, "ascii")
           r, s = DSA.sign(M, self.p, self.q, self.g, self.__x)
           return r,s
     @staticmethod
     def  createOTP(word):
         number = Helper.wordToNum(word)
         randForMult=random.sample(range(0,int(number/2)), 1)                  
         randNum= random.sample(range(number, abs(number + randForMult[0])), 1)
         return Helper.numToWord(randNum[0])
     
     @staticmethod
     def roundDown(x):
      return int(math.floor(x / 1000000000000000000.0)) * 1000000000000000000
  
     @staticmethod
     def  createOTPBig():
         retStr=""
         for i in range(100):
             number= sys.maxsize
             randNum= random.sample(range(Player.roundDown(number), number ), 1)
             retStr=retStr+Helper.numToWord(randNum[0])    
         return retStr
    
        
     def testOtpSize(self,word,otp):
         if(len(word)>len(otp)):
             return False
         else:
             return True
         
            
     def encryptStringOTP(self,word,name):
        if(name  not in self.__otpDic ):
            print(self.name+": dosent have otp for "+name)   
            return None
        if(not   self.testOtpSize(word,self.__otpDic[name])):
            print(self.name+":plane  text to large ")
            return None
        ctext=OTPBacedOnVigenereCipher.encrypt(word ,self.__otpDic[name])
        self.removeKeyFromOtpDic(name)#removing otp - cus it was used 
        return ctext   
    
     def encryptIntOTP(self,num,name):
          word=Helper.numToWord(num)
          return self.encryptStringOTP(word,name)
          
         
         
     def  decryptAsStringOTP(self, cword,name):
     
         if(name  not in self.__otpDic ):
            print(self.name+": dosent have otp for "+name)   
            return None
         if(not   self.testOtpSize(cword,self.__otpDic[name])):
            print(self.name+":cypher text to large ")
            return None
             
         text=OTPBacedOnVigenereCipher.decrypt(cword ,self.__otpDic[name])
         self.removeKeyFromOtpDic(name)#removing otp - cus it was used 
         return text
     
     def decryptAsIntOTP(self, cword,name): 
          return Helper.wordToNum(self.decryptAsStringOTP(cword,name))
     
     def removeKeyFromOtpDic(self,key):
          r = dict(self.__otpDic)
          del r[key]
          self.__otpDic=r 
          
     #unsafe cypto wise   
     def addKeyToOtpDic(self,name,key):
         self.__otpDic[name]=key
     
 #------------------------------------testing ------------------------------------------------------------------------------------------------------------
@deprecated( reason="You should use testingOpt") 
def testingEncryptDecrypt():
    
   player =Player("someting", 1, 1, 1,"test")
   ctext ,key=  player.encryptInt(45)
   text=player.decryptAsNum( ctext ,key)
   print(text)
   
   ctext ,key=  player.encryptString("planetext")
   text=player.decryptAsString( ctext ,key)
   print(text)
   
def testingOpt():

     otp =Player.createOTPBig()
     
     dictTest={}
     dictTest["somename"]=otp  
     print(dictTest)
     player =Player("testpalyer", 3,17 , 11,dictTest)
     ctext=player.encryptStringOTP("thing","somename")
     print(ctext)
     print(player.decryptAsStringOTP(ctext,"somename"))
     print(dictTest)
     player =Player("testpalyer", 3,17 , 11,dictTest)
     print(player.decryptAsStringOTP(ctext,"somename"))
     
def testingOTPIntegerEncryptDecrypt():
    
     otp =Player.createOTPBig()
     dictTest={}
     dictTest["somename"]=otp  
     #print(dictTest)
     player =Player("testpalyer", 3,17 , 11,dictTest)
     ctext=player.encryptIntOTP(123456,"somename")
     print(ctext)
     player =Player("testpalyer2", 3,17 , 11,dictTest)
     print(player.decryptAsIntOTP(ctext,"somename"))
     #print(dictTest)


 
if __name__ == '__main__': 
  #a=sys.version
  #print(Player.createOTPBig())
  #testingOpt()
  testingOTPIntegerEncryptDecrypt()