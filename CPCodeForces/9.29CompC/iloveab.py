def main():
    casenum = 0
    testcases = int(input(""))
    while casenum < testcases:
        boolcheck = True
        index = 0
        word = input()
        acount = 0
        bcount = 0
        if word[0] == "B":
            print("NO")
            casenum = casenum + 1
            continue
        if word[len(word)-1] == "A":
            print("NO")
            casenum = casenum + 1
            continue
        while index < len(word):
            if word[index] == "A":
                acount = acount+1
            if word[index] == "B":
                bcount = bcount + 1
            if bcount > acount:
                print("NO")
                boolcheck = False
                break
            index = index + 1
        if boolcheck == True:
            print("YES")
        casenum = casenum + 1
            
main()
        
        
        
    


