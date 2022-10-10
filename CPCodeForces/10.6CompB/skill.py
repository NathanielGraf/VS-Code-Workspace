def main():
    casenum = 0
    slist = []
    i = 0
    dlist = []
    firelist = []
    frostlist = []
    totaldamage = 0
    testcases = int(input())
    while casenum < testcases:
        skillnum = int(input())
        for i in range(skillnum):
            slist.append(int(input()))
        for i in range(skillnum):
            dlist.append(int(input()))
        
    for index, x in enumerate(slist):
        if x == 0:
            firelist.append(dlist[index])
        else:
            frostlist.append(dlist[index])
    
    firelist.sort()
    frostlist.sort()
    
    if firelist[-1] > frostlist[-1]:
        while frostlist and firelist:
            if frostlist:
                totaldamage = totaldamage + firelist[-1] * 2
                firelist.pop(-1)
            
            
            
        
    '''
    Take the biggest damage skill
    Put the largest damage opposite damage skill before it
    Put the largest damage opposite damage skill before it
    Repeat
    
    
    
    '''
        
        
            
main()