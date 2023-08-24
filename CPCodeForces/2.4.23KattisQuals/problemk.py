

def main():
    

    x = input()
    
    list = [int(i) for i in x.split()]
    
    #x is the first int, y is the second int, z is the third int
    
    x = list[0]
        
    y = list[1]
    
    z = list[2]
    
    #answerlist is the list of all possible answers
    
    answerlist = []
    
    #Find all possible answers
    
    #Addition
    
    answerlist.append((x + y) + z)

    answerlist.append((x + y) - z)
    
    answerlist.append((x - y) + z)
    
    answerlist.append((x - y) - z)
    
    #Multiplication
    
    answerlist.append((x * y) + z)
    
    answerlist.append((x * y) - z)
    
    answerlist.append((x - y) * z)
    
    answerlist.append((x + y) * z)
    
    #Division, the answer must be an integer, so if the answer is not an integer, do not add it to the list
    
    if (x+y)%z == 0:
        
        answerlist.append((x + y) / z)
        
    if (x*y)%z == 0:
        
        answerlist.append((x * y) / z)
        
    if (x%y == 0) and (x/y)%z == 0:
        
        answerlist.append((x / y) / z)
        
    if (x-y)%z == 0:
        
        answerlist.append((x - y) / z)
        
    
    
    return 0

main()