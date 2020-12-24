import Operations.shamir as shamir
import Operations.DSA as DSA
import Player as P

import time

class Dealer(P.Player):
    
    publicSharedPart={}
    #note: for now p is a constant in shamir.py and any body can acces it witch is fine 
    def __init__(self, name, p, q, g,t = 4,n= 5,secret = 1234 ):
         self._t=t
         self._n=n
         self.keysLeftToGive=n
         self.__shares = shamir.generateShares(n, t, secret)
         super().__init__(name, p, q, g) 
    
    #to get Rocket share sign "givemeshare" 
    def getRocketShare(self, name,r,s): 
        if(not super().IdUser(name,"givemeshare",r,s)):
            return None
        if(self.keysLeftToGive==0):
            print("Dealer: no more keys")
            return None
        
        self.publicSharedPart[name]=self.__shares[self.keysLeftToGive-1][0]
        self.keysLeftToGive=self.keysLeftToGive-1
        
        #encrypting the private part
        private,key=super().encryptInt(self.__shares[self.keysLeftToGive-1][1])
        ret=[]
        ret.append(self.__shares[self.keysLeftToGive-1][0])
        ret.append(private)
        ret.append(key)
        #TODO: add Signature 
        return ret
        
     
#------------------------------------testing ------------------------------------------------------------------------------------------------------------

def testingIdUser():
            N = 160
            L = 1024
            p, q, g = DSA.generate_params(L, N)
           
            x, y = DSA.generate_keys(g, p, q)
        
            text = "MISIS rocks"
            M = str.encode(text, "ascii")
            r, s = DSA.sign(M, p, q, g, x)
            
            
            d = Dealer("Dealer", p=p,q=q,g=g)
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
      
      d= Dealer("Dealer", p=p,q=q,g=g)
      
      d.receiveSignaturePublicKey(y, "name")
      
      shares =[]
      
      share=[]
      ret =d.getRocketShare("name",r,s)
      private =d.decryptAsNum(ret[1], ret[2])
      share.append(ret[0])
      share.append(private)
      shares.append(share)
      
      share=[]
      ret =d.getRocketShare("name",r,s)
      private =d.decryptAsNum(ret[1], ret[2])
      share.append(ret[0])
      share.append(private)
      shares.append(share)
      
      share=[]
      ret =d.getRocketShare("name",r,s)
      private =d.decryptAsNum(ret[1], ret[2])
      share.append(ret[0])
      share.append(private)
      shares.append(share)
     
      share=[]
      ret =d.getRocketShare("name",r,s)
      private =d.decryptAsNum(ret[1], ret[2])
      share.append(ret[0])
      share.append(private)
      shares.append(share)

      res =shamir.reconstructSecret(shares)
      print(d.keysLeftToGive)
      print(res)
     
if __name__ == '__main__': 
      #testingIdUser()
      testingShareDistribution()
        
     
    
   
    
   
    
          
          