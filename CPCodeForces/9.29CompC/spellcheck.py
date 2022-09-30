def main():
    timurset = {"T", "i", "m", "u", "r"}
    seenlist = set()
    casenum = 0
    testcases = int(input(""))
    while casenum < testcases:
        seenlist = set()
        index = 0
        strlength = int(input())
        word = input()
        while index < strlength:
            
            if word[index] in timurset and word[index] not in seenlist:
                boolcheck = True
            else: 
                print("NO")
                boolcheck = False
                break
            seenlist.add(word[index])
            index = index + 1
        if boolcheck == True:
            print("YES")
        casenum = casenum + 1
            
main()
        
        
        
    


