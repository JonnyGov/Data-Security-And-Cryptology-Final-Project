#1234 -> bcde
def numToWord(num):
    tempList=[]
    word=""
    [tempList.append(int(d)) for d in str(num)]
    for l in tempList:
        word=word + chr(ord('a')+l)
    return(word)
#bcde->1234         
def wordToNum(word):
    integers=[]
    for l in word:
        integers.append(ord(l)-ord('a'))         
    strings = [str(integer) for integer in integers]
    a_string = "".join(strings)
    an_integer = int(a_string)
    return an_integer
    

def testWodrNumConvertions():
    word=numToWord(1234)
    print(word)
    
    num =wordToNum(word)
    print(num)



if __name__ == '__main__': 
    testWodrNumConvertions()
    
    
