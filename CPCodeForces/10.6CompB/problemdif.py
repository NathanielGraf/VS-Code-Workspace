def main():
    i = 0
    students = int(input())
    slist = []
    while i < students:
        slist.append(int(input()))
        i = i + 1
    i = len(slist)-1
    problems = 0
    while i >= 1:
        problems = problems + (slist[i]-slist[i-1])
        i = i - 2
    return(problems)
        
        
            
main()