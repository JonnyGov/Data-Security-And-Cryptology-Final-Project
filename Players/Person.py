import Operations.DSA as DSA
import Helper
import Operations.OTPBacedOnVigenereCipher as OTPBacedOnVigenereCipher
import random
import Players.Player as P
import Players.Dealer as D

class Person(P.Player):
    __shared=[]
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
         #print(templist)
         
    def giveShareToRocket(self,rocketName):
         ret=[]
         ret.append(self.__shared[0])
         private =super().encryptIntOTP(self.__shared[1],rocketName)
         r,s=super().sign(private)
         ret.append(private)
         ret.append(r)
         ret.append(s)
         return ret #ret[0-public share][1-private share][2-r][3-s]
         



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
      
def testGiveShareToRocket():
      N = 160
      L = 1024
      p, q, g = DSA.generate_params(L, N)
           

        
      
      
      perosnName="Person"
      DealerName= "Dealer"
      rocketName="rocket"
      
      dictTest={}
      otp =P.Player.createOTPBig()
      dictTest[DealerName]=otp
      dictTest[perosnName]=otp  
      dictTest[rocketName]=otp 
      #print(otp)
      #print(dictTest) 
      
      d=D.Dealer(DealerName, dictTest, dictTest, p, q, g) 
      person= Person(p, q, g, perosnName, dictTest)
      
      d.receiveSignaturePublicKey(person.y,person.name)
      person.receiveSignaturePublicKey(d.y,d.name)
      #givemeshare
      r,s=person.sign("givemeshare")
      ret=d.getRocketShare(person.name,r, s)
      
      person.receiveShare(ret, d.name)
      
      rocket =P.Player(rocketName, p, q, g, dictTest)
      
      person.receiveSignaturePublicKey(rocket.y, rocket.name)
      ret=person.giveShareToRocket(rocketName)
      print(ret[1])
      print(rocket.decryptAsIntOTP(ret[1], perosnName))
      
    
    
if __name__ == '__main__': 
    
    #testReceiveShare()
    testGiveShareToRocket()
        
        
    
        
        
   
            
            
        
        
        