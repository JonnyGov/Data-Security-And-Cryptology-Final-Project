import Operations.shamir as shamir
import Operations.DSA as DSA
import Player as P
import Helper 
import time
import sys
from deprecated import deprecated
import Operations.OTPBacedOnVigenereCipher as OTPBacedOnVigenereCipher

class Dealer(P.Player):
    
    publicSharedPart={}
    #note: for now p is a constant in shamir.py and any body can acces it witch is fine 
    def __init__(self, name,otpDic,otpDicRokcet, p, q, g,t = 4,n= 5,secret = 1234 ):
         self._t=t
         self._n=n
         self.keysLeftToGive=n
         self.__secret=secret
         self.__shares = shamir.generateShares(n, t, secret)
         self.__otpDicRokcet=otpDicRokcet # only players who are allowed to have the seacret
         
         super().__init__(name, p, q, g,otpDic) 
    
    #to get shamir share person needs to  sign "givemeshare" 
    #note dealer singns the encrypted private part of the shamir shear
    def getRocketShare(self, name,r,s): 
        if(not super().IdUser(name,"givemeshare",r,s)):
            return None
        if(self.keysLeftToGive==0):
            print("Dealer "+self.name +": no more keys")
            return None


        self.publicSharedPart[name]=self.__shares[self.keysLeftToGive-1][0]
        self.keysLeftToGive=self.keysLeftToGive-1
        
        #encrypting the private part
        forTesting=self.__shares[self.keysLeftToGive-1][1]
        forTesting2=sys.maxsize
        privateAsString= Helper.numToWord(self.__shares[self.keysLeftToGive-1][1])
        private=super().encryptStringOTP(privateAsString,name)
        if(private==None):
            print(self.name+": dosen know "+name)
            return None
        ret=[]
        ret.append(self.__shares[self.keysLeftToGive-1][0])
        ret.append(private)
        r,s=super().sign(private)
        ret.append(r)
        ret.append(s)
        return ret #ret=[0-public part of shamir][1-encrypted privte part of shamir][2-r][3-s]
    
    
    def encryptStringOTPForRocket(self,word,name):
        if(name  not in self.__otpDicRokcet ):
            print(self.name+": dosent have otp for "+name)   
            return None
        if(not   self.testOtpSize(word,self.__otpDicRokcet[name])):
            print(self.name+":plane  text to large ")
            return None
        ctext=OTPBacedOnVigenereCipher.encrypt(word ,self.__otpDicRokcet[name])
        del self.__otpDicRokcet[name] 
        return ctext   
    
    #to get seacret  the rocet needs to  sign "givemeSeacret" 
    def getSeacret(self, name,r,s): 
        if(not super().IdUser(name,"givemeseacret",r,s)):
            return None
        privateAsString= Helper.numToWord(self.__secret)
        private=self.encryptStringOTPForRocket(privateAsString,name)
        return private
    
        
        #return ret #ret=[0-public part of shamir][1-encrypted privte part of shamir][2-key for private part][3-r][4-s]
        
     
#------------------------------------testing ------------------------------------------------------------------------------------------------------------
@deprecated( reason="dealer changed to match")
def testingIdUser():
            N = 160
            L = 1024
            p, q, g = DSA.generate_params(L, N)
           
            x, y = DSA.generate_keys(g, p, q)
        
            text = "MISIS rocks"
            M = str.encode(text, "ascii")
            r, s = DSA.sign(M, p, q, g, x)
            
            dictTest={}
            otp =P.Player.createOTPBig()
            d = Dealer("Dealer",dictTest, p=p,q=q,g=g)
            d.receiveSignaturePublicKey(y, "test")
            d.IdUser("test", text, r, s)

def testingShareDistribution():
      N = 160
      L = 1024
      p, q, g = DSA.generate_params(L, N)
           
      x, y = DSA.generate_keys(g, p, q)
        
      text = "givemeshare"
      M = str.encode(text, "ascii")
      r, s = DSA.sign(M, p, q, g, x)      
      
      
      dictTest={}
      otp =P.Player.createOTPBig()
      dictTest["Dealer4"]=otp
      otp =P.Player.createOTPBig()
      dictTest["Dealer1"]=otp  
      otp =P.Player.createOTPBig()
      dictTest["Dealer2"]=otp 
      otp =P.Player.createOTPBig()
      dictTest["Dealer3"]=otp  
     
      #print(otp)
      #print(dictTest) 
        
      d= Dealer("Dealer",dictTest, p=p,q=q,g=g)
      d1= Dealer("Dealer1",dictTest, p=p,q=q,g=g)
      d2= Dealer("Dealer2",dictTest, p=p,q=q,g=g)
      d3= Dealer("Dealer3",dictTest, p=p,q=q,g=g)
      d4= Dealer("Dealer4",dictTest, p=p,q=q,g=g)
      
      d.receiveSignaturePublicKey(y, "Dealer")
      d.receiveSignaturePublicKey(y, "Dealer1")
      d.receiveSignaturePublicKey(y, "Dealer2")
      d.receiveSignaturePublicKey(y, "Dealer3")
      d.receiveSignaturePublicKey(y, "Dealer4")
      
      shares =[]
      
      share=[]
      ret =d.getRocketShare("Dealer1",r,s)
      private =d1.decryptAsStringOTP(ret[1], "Dealer1")
      share.append(ret[0])
      share.append(Helper.wordToNum(private))
      shares.append(share)
      #testing singneture
      d.receiveSignaturePublicKey(d.y,d.name)
      answer =d.IdUser(d.name,ret[1],ret[2],ret[3])
      print(answer)
  
      #
      
      share=[]
      ret =d.getRocketShare("Dealer2",r,s)
      private =d2.decryptAsStringOTP(ret[1], "Dealer2")
      share.append(ret[0])
      share.append(Helper.wordToNum(private))
      shares.append(share)
      
      share=[]
      ret =d.getRocketShare("Dealer3",r,s)
      private =d3.decryptAsStringOTP(ret[1], "Dealer3")
      share.append(ret[0])
      share.append(Helper.wordToNum(private))
      shares.append(share)
     
      share=[]
      ret =d.getRocketShare("Dealer4",r,s)
      private =d4.decryptAsStringOTP(ret[1], "Dealer4")
      share.append(ret[0])
      share.append(Helper.wordToNum(private))
      shares.append(share)
      
      
      print(shares)
      res =shamir.reconstructSecret(shares)
      print("the amount of keys left: " + str(d.keysLeftToGive))
      print(res)
      
      text = "givemeseacret"
      M = str.encode(text, "ascii")
      r, s = DSA.sign(M, p, q, g, x) 
      
def testGetSeacret():
      N = 160
      L = 1024
      p, q, g = DSA.generate_params(L, N)
           
      x, y = DSA.generate_keys(g, p, q)
        
      text = "givemeseacret"
      M = str.encode(text, "ascii")
      r, s = DSA.sign(M, p, q, g, x)      
      
      
      dictTest={}
      otp =P.Player.createOTPBig()
      dictTest["Dealer"]=otp
      dictTest["Dealer2"]=otp  
     
      #print(otp)
      #print(dictTest) 
        
      d= Dealer("Dealer",dictTest,dictTest, p=p,q=q,g=g)

      
      d.receiveSignaturePublicKey(y, "Dealer")
      cword= d.getSeacret( "Dealer",r,s)

      d.receiveSignaturePublicKey(y, "Dealer2")
      
      d2= Dealer("Dealer2",dictTest,dictTest, p=p,q=q,g=g)
      
      ptext=d2.decryptAsStringOTP(cword, "Dealer2")
      secret=Helper.wordToNum(ptext)
      print(str(secret) +" "+cword) 

if __name__ == '__main__': 
      #testingIdUser()
      #testingShareDistribution()
      testGetSeacret()
        
     
    
   
    
   
    
          
          