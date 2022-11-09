

def main():
    numberofboxes = int(input(""))
    x = str(input())
    i = 0
    boxvals = [int(i) for i in x.split()]
    boxvals.sort()
    #For each number, if there is a duplicate number, add 1 to one number and remove the other
    swap = 1
    while swap == 1:
        swap = 0
        i = 0
        while i < len(boxvals)-1:
            if len(boxvals) <= 2:
                print("Y")
                return 0
        
            elif boxvals[i] == boxvals[i+1]:
                boxvals[i] = boxvals[i] + 1
                boxvals.pop(i+1)
                i = i - 1
                swap = 1
            i = i + 1
   
    print("N")
    return 0
    


            
main()
