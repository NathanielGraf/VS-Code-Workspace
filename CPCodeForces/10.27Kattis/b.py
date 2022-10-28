#* and 
#+ or
#- not




def main():
    inputvariables = int(input(""))
    hashmap = {}
    x = str(input())
    i = 0
    truefalse = [str(i) for i in x.split()]
    while i < len(truefalse):
        if truefalse[i] == "T":
            truefalse[i] = 1
        else:
            truefalse[i] = 0
        i = i + 1
    
    circuit = str(input())
    
    circuitlist = [str(i) for i in circuit.split()]
    
    for i in range(inputvariables):
        
        hashmap[chr(ord("A") + i)] = truefalse[i]
    
    hashmap[0] = 0
    hashmap[1] = 1

    print(hashmap)
    
    
            
    while(len(circuitlist)!= 1):
        for index, char in enumerate(circuitlist):
            print(circuitlist)
            print(circuitlist[index])
            if char in hashmap:
                if circuitlist[index+2] == "*":
                    if hashmap[circuitlist[index]] and hashmap[circuitlist[index + 1]]:
                        circuitlist.pop(index)
                        circuitlist.pop(index)
                        circuitlist.pop(index)
                        circuitlist.insert(index, 1)
                    else:
                        circuitlist.pop(index)
                        circuitlist.pop(index)
                        circuitlist.pop(index)
                        circuitlist.insert(index, 0)
                    
                elif circuitlist[index+2] == "+":
                    if hashmap[circuitlist[index]] or hashmap[circuitlist[index + 1]]:
                        circuitlist.pop(index)
                        circuitlist.pop(index)
                        circuitlist.pop(index)
                        circuitlist.insert(index, 1)
                    else:
                        circuitlist.pop(index)
                        circuitlist.pop(index)
                        circuitlist.pop(index)
                        circuitlist.insert(index, 0)
                            
                            
                if index < len(circuitlist) - 1 and circuitlist[index+1] == "-":
                    if circuitlist[index] == 0:
                        circuitlist[index] = 1 
                    else:
                        circuitlist[index] = 0
                    circuitlist.pop(index+1)
            else:
                continue
                
    if circuitlist[0] == 0:
        print("F")
        return
    else:
        print("T")
        return
main()
