import Operations.shamir as shamir
import Players.Person as Person
import Operations.DSA as DSA
import Players.Rocket as Rocket


def main():
  # (3,5) sharing scheme 
    t,n = 4, 5
    secret = 1235
    print('Original Secret:', secret) 
   
    # Phase I: Generation of shares 
    shares = shamir.generateShares(n, t, secret) 
    print('\nShares:', *shares) 
    #Phase II: DSA
    N = 160
    L = 1024
    p, q, g = DSA.generate_params(L, N)
    
    ##
    p1= Person.Person( shares[0], p, q, g ,"person1")
    p2= Person.Person( shares[1], p, q, g ,"person2")
    p3= Person.Person( shares[2], p, q, g ,"person3")
    p4= Person.Person( shares[3], p, q, g ,"person4")
    
    r1=Rocket.Rocket(secret, p, q, g, "rocket")
    r1.receivePublicKey(p1.y,"perosn1")
    r1.receivePublicKey(p2.y,"perosn2")
    r1.receivePublicKey(p3.y,"perosn3")
    r1.receivePublicKey(p4.y,"perosn4")
    
    
    #########
    
    
    
    ctext0 ,ctext1,key,ctext0RS,ctext1RS =p1.fullEncryption()
    r1.reciveShamirKeyPart("perosn1",ctext0 ,ctext1,key,ctext0RS,ctext1RS)
    
    ctext0 ,ctext1,key,ctext0RS,ctext1RS =p2.fullEncryption()
    r1.reciveShamirKeyPart("perosn2",ctext0 ,ctext1,key,ctext0RS,ctext1RS)
    
    ctext0 ,ctext1,key,ctext0RS,ctext1RS =p3.fullEncryption()
    r1.reciveShamirKeyPart("perosn3",ctext0 ,ctext1,key,ctext0RS,ctext1RS)
    
    ctext0 ,ctext1,key,ctext0RS,ctext1RS =p4.fullEncryption()
    r1.reciveShamirKeyPart("perosn4",ctext0 ,ctext1,key,ctext0RS,ctext1RS)
    
    print(r1.reconstructSecret())
    
    




main()