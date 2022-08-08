def answer():
    #Defines number of test cases
    T = 2
    
    #Loop through all test cases
    for z in range(1, T+1):
        
        #Define string to test
        string = "AABCAAAAA"
        
        #Turn string into list for ease of editing
        stringlist = [n for n in string]
        
        #Define variables
        i = 0
        x = 1
        
        #Loop through length of stringlist
        while i < len(stringlist)-1:
            
            #If on the last letter in the list, break loop
            if i == len(stringlist) - 1:
                break
            
            #If the current letter is the same as the next, add one to the copy count (x), and move to next letter
            elif stringlist[i] == stringlist[i+1]:
                i = i + 1
                x = x + 1 
            
            #If the current letter comes before the next, duplicate it by the value of the copy amount, then skip to next
            elif stringlist[i] < stringlist[i+1]: 
                stringlist.insert(i, stringlist[i]*x)
                x = 1
                i = i + 2
            
            #If neither of above are true (current is greater than next), skip
            else:
                i = i + 1 
                x = 1
        
        #Turns list into string    
        answer = "".join(stringlist)
        
        #Prints case info
        print("Case #" + str(z) + ": " + str(answer))   

#Runs function
answer()
