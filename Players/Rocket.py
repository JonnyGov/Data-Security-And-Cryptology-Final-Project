
import Operations.DSA as DSA
import Helper
import Operations.OTPBacedOnVigenereCipher as OTPBacedOnVigenereCipher
import random
import Operations.shamir as shamir
import Player as P
class Rocket(P.Player):
    shamirParts=[]
    def __init__(self, p, q, g ,name,otpDic):
             # p, q, g - parms for signuture
            super().__init__(name, p, q, g,otpDic) 
            
    def reciveShamirSecret(self,dealerName,secretEncrypted,dealerR,dealerS):
        if(not super().IdUser(dealerName,secretEncrypted,dealerR,dealerS)):
            return False
        self.__secret=super().decryptAsIntOTP(secretEncrypted,dealerName)
        return True
    def reciveShare(self,personName,personR,personS,share):
        # test if there are already 4 persons shares.
        if (len(self.shamirParts))>=4:
            return False
        # share -> [0] not encrypted ; [1] encrypted
        if(not super().IdUser(personName,share[1],personR,personS)):
            return False
        temp=super().decryptAsIntOTP(share[1],personName)
        if temp is not None:
            self.shamirParts.append(list(share[0],temp))
            self._launch(self)
    
    def _launch(self):
         if (len(self.shamirParts))<4: 
             return False
         temp=shamir.reconstructSecret(self.shamirParts)
         if (temp is self.__secret):
             self._launchEvent()
             return True
    def _launchEvent():
        print("rocket launched!")
        
##-----------------------------TEST---------------------------------------
if __name__ == '__main__':
    import Dealer as D
    N = 160
    L = 1024
    p, q, g = DSA.generate_params(L, N)
    name, otpDic, otpDicRokcet="deal",{},{}
    
    otp=P.Player.createOTPBig()
    otpDicRokcet["rocket"]=otp
    dealer=D.Dealer(name, otpDic, otpDicRokcet, p, q, g)
    otpDic[dealer.name]=otp
    rocket= Rocket(p, q, g,"rocket",otpDic)
    rocket.receiveSignaturePublicKey(dealer.y,dealer.name)
    dealer.receiveSignaturePublicKey(rocket.y,rocket.name)
    r,s=rocket.sign("givemeseacret")
    ret= dealer.getSeacret(rocket.name,r,s)
    #ret=[0-encrypted seacret][1-r][2-s]
    rocket.reciveShamirSecret(dealer.name,ret[0],ret[1],ret[2])
    
    
   
    
    
    