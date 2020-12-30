
import Operations.DSA as DSA
import Helper
import Operations.OTPBacedOnVigenereCipher as OTPBacedOnVigenereCipher
import random
import Operations.shamir as shamir
import Players.Player as P
import time
class Rocket(P.Player):
    shamirParts=[]
    def __init__(self, p, q, g ,name,otpDic):
             # p, q, g - parms for signuture
            super().__init__(name, p, q, g,otpDic) 
            
    def reciveShamirSecret(self,dealerName,secretEncrypted,dealerR,dealerS):
        if(not super().IdUser(dealerName,secretEncrypted,dealerR,dealerS)):
            return False
        self._secret=super().decryptAsIntOTP(secretEncrypted,dealerName)
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
            self.shamirParts.append((share[0],temp))
            self._launch()
    
    def _launch(self):
         if (len(self.shamirParts))<4: 
             return False
         temp=shamir.reconstructSecret(self.shamirParts)
         if (temp == self._secret):
             self._launchEvent()
             return True
    def _launchEvent(self):
        for  i in reversed(range(11)):
            time.sleep(0.5)
            print(i)
        print("  /\ \n /  \ \n |  | \n |  | \n/ == \ \n|/**\| ")
        
##-----------------------------TEST---------------------------------------

def __receiveShare(player,share,name):#share=[0-public part of shamir][1-encrypted privte part of shamir][2-r][3-s]
         if(not player.IdUser(name,share[1],share[2],share[3])):
            return None
         private =player.decryptAsStringOTP(share[1],name)
         templist=[]
         templist.append(share[0])
         templist.append(Helper.wordToNum(private))
         player.__shared=templist
         player.publicShare=templist[0]
         return templist
def __giveShare(player,share,name):#share=[0-public part of shamir][1-decrypted privte part of shamir][2-r][3-s]
         private =player.encryptIntOTP(share[1],name)
         templist=[]
         templist.append(share[0])
         templist.append(private)
         player.__shared=templist
         player.publicShare=templist[0]
         return templist
if __name__ == '__main__':
    import Dealer as D
    import Person as Pr
    N = 160
    L = 1024
    p, q, g = DSA.generate_params(L, N)
    dealerName="deal"
    rocketName="rocket"
    p1Name="p1"
    p2Name="p2"
    p3Name="p3"
    p4Name="p4"
    otpDicRokcet={} # for dealer (rocket)
    otpDicDealer={} # for dealer (person)
    dictTest2={} # for rocket
    dictP1={} # for person p1
    dictP2={} # for person p2
    dictP3={} # for person p3
    dictP4={} # for person p4
    
    #otp for rocket and dealer
    otp=P.Player.createOTPBig()
    otpDicRokcet[rocketName]=otp
    dictTest2[dealerName]=otp
    
    #p1
    #otp for dearl and person
    otp =P.Player.createOTPBig()
    dictP1[dealerName]=otp
    otpDicDealer[p1Name]=otp 
    
    #otp for rocket and person
    otp =P.Player.createOTPBig()
    dictTest2[p1Name]=otp
    dictP1[rocketName]=otp
    
    #p2
    #otp for dearl and person
    otp =P.Player.createOTPBig()
    dictP2[dealerName]=otp
    otpDicDealer[p2Name]=otp 
    
    #otp for rocket and person
    otp =P.Player.createOTPBig()
    dictTest2[p2Name]=otp
    dictP2[rocketName]=otp
    
    #p3
    #otp for dearl and person
    otp =P.Player.createOTPBig()
    dictP3[dealerName]=otp
    otpDicDealer[p3Name]=otp 
    
    #otp for rocket and person
    otp =P.Player.createOTPBig()
    dictTest2[p3Name]=otp
    dictP3[rocketName]=otp
    
    #p4
    #otp for dearl and person
    otp =P.Player.createOTPBig()
    dictP4[dealerName]=otp
    otpDicDealer[p4Name]=otp 
    
    #otp for rocket and person
    otp =P.Player.createOTPBig()
    dictTest2[p4Name]=otp
    dictP4[rocketName]=otp
    
    dealer=D.Dealer(dealerName, otpDicDealer, otpDicRokcet, p, q, g)
    
    rocket= Rocket(p, q, g,rocketName,dictTest2)
    
    p1=Pr.Person(p, q, g, p1Name, dictP1)
    p2=Pr.Person(p, q, g, p2Name, dictP2)
    p3=Pr.Person(p, q, g, p3Name, dictP3)
    p4=Pr.Person(p, q, g, p4Name, dictP4)
    
    
    rocket.receiveSignaturePublicKey(dealer.y,dealer.name)
    rocket.receiveSignaturePublicKey(p1.y,p1.name)
    rocket.receiveSignaturePublicKey(p2.y,p2.name)
    rocket.receiveSignaturePublicKey(p3.y,p3.name)
    rocket.receiveSignaturePublicKey(p4.y,p4.name)
    
    dealer.receiveSignaturePublicKey(rocket.y,rocket.name)
    dealer.receiveSignaturePublicKey(p1.y,p1.name)
    dealer.receiveSignaturePublicKey(p2.y,p2.name)
    dealer.receiveSignaturePublicKey(p3.y,p3.name)
    dealer.receiveSignaturePublicKey(p4.y,p4.name)
    
    p1.receiveSignaturePublicKey(dealer.y,dealer.name)
    p1.receiveSignaturePublicKey(rocket.y,rocket.name)
    
    p2.receiveSignaturePublicKey(dealer.y,dealer.name)
    p2.receiveSignaturePublicKey(rocket.y,rocket.name)
    
    p3.receiveSignaturePublicKey(dealer.y,dealer.name)
    p3.receiveSignaturePublicKey(rocket.y,rocket.name)
    
    p4.receiveSignaturePublicKey(dealer.y,dealer.name)
    p4.receiveSignaturePublicKey(rocket.y,rocket.name)
    
    # get secret from dealer to rocket
    r,s=rocket.sign("givemeseacret")
    ret= dealer.getSeacret(rocket.name,r,s)
    #ret=[0-encrypted seacret][1-r][2-s]
    rocket.reciveShamirSecret(dealer.name,ret[0],ret[1],ret[2])
    
    #get shares from dealer to persons
    r,s=p1.sign("givemeshare")
    ret= dealer.getRocketShare(p1.name,r,s)
   # p1.receiveShare(ret,dealer.name)
    sharesP1=__receiveShare(p1,ret,dealer.name)
    
    r,s=p2.sign("givemeshare")
    ret= dealer.getRocketShare(p2.name,r,s)
   # p2.receiveShare(ret,dealer.name)
    sharesP2=__receiveShare(p2,ret,dealer.name)
    
    r,s=p3.sign("givemeshare")
    ret= dealer.getRocketShare(p3.name,r,s)
   # p3.receiveShare(ret,dealer.name)
    sharesP3= __receiveShare(p3,ret,dealer.name)
    
    r,s=p4.sign("givemeshare")
    ret= dealer.getRocketShare(p4.name,r,s)
   # p4.receiveShare(ret,dealer.name)
    sharesP4=__receiveShare(p4,ret,dealer.name)
    
    
    sharesP1= __giveShare(p1,sharesP1,rocket.name)
    r,s=p1.sign(sharesP1[1])
    rocket.reciveShare(p1.name,r,s,sharesP1)
    
    sharesP2= __giveShare(p2,sharesP2,rocket.name)
    r,s=p2.sign(sharesP2[1])
    rocket.reciveShare(p2.name,r,s,sharesP2)
    
    sharesP3= __giveShare(p3,sharesP3,rocket.name)
    r,s=p3.sign(sharesP3[1])
    rocket.reciveShare(p3.name,r,s,sharesP3)
    
    sharesP4= __giveShare(p4,sharesP4,rocket.name)
    r,s=p4.sign(sharesP4[1])
    rocket.reciveShare(p4.name,r,s,sharesP4)
    
   
    
    
    