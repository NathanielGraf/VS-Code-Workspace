

import string


def encrypt(string):
    stringarray = list(string)
    #print(stringarray)
    stringarray.pop(0)
    stringarray.pop(0)
    #print(stringarray)
    valuearray = []
    for index, char in enumerate(stringarray):
        #print(ord(char)-96, end = ' ')
        if index == 0:
            valuearray.append(ord(char)-96)
        elif char == ' ':
            valuearray.append(valuearray[index-1])
        else:
            valuearray.append(ord(char)-96 + valuearray[index-1])
    #print(valuearray)
    for i in valuearray:
        if i % 27 == 0:
            print(' ', end = '')
        else:
            print(chr(i%27 + 96), end='')
    #print("\n")
        
        #print(string.ascii_lowercase[i%27-1], end='')
        
def decrypt(string):
    
    stringarray = list(string)
    stringarray.pop(0)
    stringarray.pop(0)
    #print(stringarray)
    
    modarray = []
    letterarray = []
    for x in stringarray:
        if x == ' ':
            modarray.append(0)
        else:
            modarray.append(ord(x) - 96)
    #print(modarray)
    for index, num in enumerate(modarray):
        if index == 0:
            letterarray.append(num)
        else:
            letterarray.append((num - modarray[index-1] + 27)%27)
    #print(letterarray)
            
    #print(letterarray)
    for i in letterarray:
        if i == 0:
            print(" ", end = '')
        else:
            print(chr(i+96), end='')
    #print("\n")


def main():
    casenum = 0
    testcases = int(input(""))
    while casenum < testcases:
        casenum += 1
        string = input("")
        
        if string[0] == "e":
            encrypt(string)
            print("")
            
        elif string[0] == "d":
            decrypt(string)
            print("")
        
            
main()
        
        
        
    


