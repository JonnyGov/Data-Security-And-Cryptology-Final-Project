def numToWord(num):
    tempList=[]
    word=""
    [tempList.append(int(d)) for d in str(num)]
    for l in tempList:
        word=word + chr(ord('a')+l)
    return(word)
         
def wordToNum(word):
    integers=[]
    for l in word:
        integers.append(ord(l)-ord('a'))         
    strings = [str(integer) for integer in integers]
    a_string = "".join(strings)
    an_integer = int(a_string)
    return an_integer
    


if __name__ == '__main__': 
    word=numToWord(1234)
    print(word)
    
    num =wordToNum(word)
    print(num)
