import Operations.DSA as DSA
import Helper
import Operations.OTPBacedOnVigenereCipher as OTPBacedOnVigenereCipher
import random
import Player as P
import Dealer as D

class Person(P.Player):
    
    def __init__(self, p, q, g ,name,otpDic):
         # p, q, g - parms for signuture
            super().__init__(name, p, q, g, otpDic)
            
    def receiveShare(self,share,name):#share=[0-public part of shamir][1-encrypted privte part of shamir][2-r][3-s]
         if(not super().IdUser(name,share[1],share[2],share[3])):
            return None
         private =super().decryptAsStringOTP(share[1],name)
         templist=[]
         templist.append(share[0])
         templist.append(Helper.wordToNum(private))
         self.__shared=templist
         self.publicShare=templist[0]
         print(templist)
         



#------------------------------------testing ------------------------------------------------------------------------------------------------------------

def testReceiveShare():
      N = 160
      L = 1024
      p, q, g = DSA.generate_params(L, N)
           
      x, y = DSA.generate_keys(g, p, q)
        
      text = "givemeshare"
      M = str.encode(text, "ascii")
      #r, s = DSA.sign(M, p, q, g, x)      
      
      
      dictTest={}
      otp =P.Player.createOTPBig()
      dictTest["Dealer"]=otp
      dictTest["person1"]=otp  
     
      #print(otp)
      #print(dictTest) 
        
      d= D.Dealer("Dealer",dictTest,dictTest, p=p,q=q,g=g)
      p1= Person( p,q,g,"person1",dictTest)
      
      d.receiveSignaturePublicKey(p1.y, "person1")
      r, s =p1.sign("givemeshare")
      
      share =d.getRocketShare("person1", r, s)
      
      p1.receiveSignaturePublicKey(d.y, "Dealer")
      p1.receiveShare(share, "Dealer")
      print(p1.publicShare)
    
    
if __name__ == '__main__': 
    
    testReceiveShare()
        
        
    
        
        
   
            
            
        
        
        