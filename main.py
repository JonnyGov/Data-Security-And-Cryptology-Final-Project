import Players.Player as Player
import Players.Person as P
import Operations.DSA as DSA
import Players.Rocket as Rocket
import Players.Dealer as D

def main():
    #inisilite security system:
        
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
    otp=Player.Player.createOTPSizeOfPirme()
    otpDicRokcet[rocketName]=otp
    dictTest2[dealerName]=otp
    
    #p1
    #otp for dearl and person
    otp =Player.Player.createOTPSizeOfPirme()
    dictP1[dealerName]=otp
    otpDicDealer[p1Name]=otp 
    
    #otp for rocket and person
    otp =Player.Player.createOTPSizeOfPirme()
    dictTest2[p1Name]=otp
    dictP1[rocketName]=otp
    
    #p2
    #otp for dearl and person
    otp =Player.Player.createOTPSizeOfPirme()
    dictP2[dealerName]=otp
    otpDicDealer[p2Name]=otp 
    
    #otp for rocket and person
    otp =Player.Player.createOTPSizeOfPirme()
    dictTest2[p2Name]=otp
    dictP2[rocketName]=otp
    
    #p3
    #otp for dearl and person
    otp =Player.Player.createOTPSizeOfPirme()
    dictP3[dealerName]=otp
    otpDicDealer[p3Name]=otp 
    
    #otp for rocket and person
    otp =Player.Player.createOTPSizeOfPirme()
    dictTest2[p3Name]=otp
    dictP3[rocketName]=otp
    
    #p4
    #otp for dearl and person
    otp =Player.Player.createOTPSizeOfPirme()
    dictP4[dealerName]=otp
    otpDicDealer[p4Name]=otp 
    
    #otp for rocket and person
    otp =Player.Player.createOTPSizeOfPirme()
    dictTest2[p4Name]=otp
    dictP4[rocketName]=otp
    
    #create dealer:
    dealer=D.Dealer(dealerName, otpDicDealer, otpDicRokcet, p, q, g)
    #create rocket:
    rocket= Rocket.Rocket(p, q, g,rocketName,dictTest2)
    #create players:
    p1=P.Person(p, q, g, p1Name, dictP1)
    p2=P.Person(p, q, g, p2Name, dictP2)
    p3=P.Person(p, q, g, p3Name, dictP3)
    p4=P.Person(p, q, g, p4Name, dictP4)
    
    #assign all sign to rocket:
    rocket.receiveSignaturePublicKey(dealer.y,dealer.name)
    rocket.receiveSignaturePublicKey(p1.y,p1.name)
    rocket.receiveSignaturePublicKey(p2.y,p2.name)
    rocket.receiveSignaturePublicKey(p3.y,p3.name)
    rocket.receiveSignaturePublicKey(p4.y,p4.name)
    #assign all sign to dealer:
    dealer.receiveSignaturePublicKey(rocket.y,rocket.name)
    dealer.receiveSignaturePublicKey(p1.y,p1.name)
    dealer.receiveSignaturePublicKey(p2.y,p2.name)
    dealer.receiveSignaturePublicKey(p3.y,p3.name)
    dealer.receiveSignaturePublicKey(p4.y,p4.name)
    
    #assign all sign to players:
    p1.receiveSignaturePublicKey(dealer.y,dealer.name)
    p1.receiveSignaturePublicKey(rocket.y,rocket.name)
    
    p2.receiveSignaturePublicKey(dealer.y,dealer.name)
    p2.receiveSignaturePublicKey(rocket.y,rocket.name)
    
    p3.receiveSignaturePublicKey(dealer.y,dealer.name)
    p3.receiveSignaturePublicKey(rocket.y,rocket.name)
    
    p4.receiveSignaturePublicKey(dealer.y,dealer.name)
    p4.receiveSignaturePublicKey(rocket.y,rocket.name)
    
    #end inisilite
    
    # get secret from dealer to rocket
    r,s=rocket.sign("givemeseacret")
    ret= dealer.getSeacret(rocket.name,r,s)
    #ret=[0-encrypted seacret][1-r][2-s]
    rocket.reciveShamirSecret(dealer.name,ret[0],ret[1],ret[2])
    
    #get shares from dealer to persons:
        
    r,s=p1.sign("givemeshare")
    ret= dealer.getRocketShare(p1.name,r,s)
    p1.receiveShare(ret,dealer.name)
    
    r,s=p2.sign("givemeshare")
    ret= dealer.getRocketShare(p2.name,r,s)
    p2.receiveShare(ret,dealer.name)

    
    r,s=p3.sign("givemeshare")
    ret= dealer.getRocketShare(p3.name,r,s)
    p3.receiveShare(ret,dealer.name)

    
    r,s=p4.sign("givemeshare")
    ret= dealer.getRocketShare(p4.name,r,s)
    p4.receiveShare(ret,dealer.name)
    
    # give share from persons to rocket:
        
    #ret[0-public share][1-private share][2-r][3-s]
    ret= p1.giveShareToRocket(rocket.name)
    rocket.reciveShare(p1.name,ret[2],ret[3],ret[0:2])
    
    ret= p2.giveShareToRocket(rocket.name)
    rocket.reciveShare(p2.name,ret[2],ret[3],ret[0:2])
    
    ret= p3.giveShareToRocket(rocket.name)
    rocket.reciveShare(p3.name,ret[2],ret[3],ret[0:2])
    
    ret= p4.giveShareToRocket(rocket.name)
    rocket.reciveShare(p4.name,ret[2],ret[3],ret[0:2])
    
   
    




main()

        