

#Returns length to add and new current position
def findNextAndCalcLength(currentNum, matrix, currPos):
    nextNum = currentNum + 1
    if currPos == 0:
        if matrix[1] == nextNum:
            return 1, 1
        elif matrix[2] == nextNum:
            return 2, 2
        elif matrix[3] == nextNum:
            return 1, 3
        elif matrix[4] == nextNum: 
            return pow(2, 0.5), 4
        elif matrix[5] == nextNum:
            return pow(5, 0.5), 5
        elif matrix[6] == nextNum:
            return 2, 6
        elif matrix[7] == nextNum:
            return pow(5, 0.5), 7
        elif matrix[8] == nextNum:
            return pow(8, 0.5), 8
    
    elif currPos == 1:
        if matrix[0] == nextNum:
            return 1, 0
        elif matrix[2] == nextNum:
            return 1, 2
        elif matrix[3] == nextNum:
            return pow(2, 0.5), 3
        elif matrix[4] == nextNum: 
            return 1, 4
        elif matrix[5] == nextNum:
            return pow(2, 0.5), 5
        elif matrix[6] == nextNum:
            return pow(5, 0.5), 6
        elif matrix[7] == nextNum:
            return 2, 7
        elif matrix[8] == nextNum:
            return pow(5, 0.5), 8
        
    elif currPos == 2:
        if matrix[0] == nextNum:
            return 2, 0
        elif matrix[1] == nextNum:
            return 1, 1
        elif matrix[3] == nextNum:
            return pow(5, 0.5), 3
        elif matrix[4] == nextNum: 
            return pow(2, 0.5), 4
        elif matrix[5] == nextNum:
            return 1, 5
        elif matrix[6] == nextNum:
            return pow(8, 0.5), 6
        elif matrix[7] == nextNum:
            return pow(5, 0.5), 7
        elif matrix[8] == nextNum:
            return 2, 8
        
    elif currPos == 3:
        if matrix[0] == nextNum:
            return 1, 0
        elif matrix[1] == nextNum:
            return pow(2, 0.5), 1
        elif matrix[2] == nextNum:
            return pow(5, 0.5), 2
        elif matrix[4] == nextNum:
            return 1, 4
        elif matrix[5] == nextNum:
            return 2, 5
        elif matrix[6] == nextNum:
            return 1, 6
        elif matrix[7] == nextNum:
            return pow(2, 0.5), 7
        elif matrix[8] == nextNum:
            return pow(5, 0.5), 8
        
    elif currPos == 4:
        if matrix[0] == nextNum:
            return pow(2, 0.5), 1
        elif matrix[1] == nextNum:
            return 1, 1
        elif matrix[2] == nextNum:
            return pow(2, 0.5), 2
        elif matrix[3] == nextNum:
            return 1, 3
        elif matrix[5] == nextNum:
            return 1, 5
        elif matrix[6] == nextNum:
            return pow(2, 0.5), 6
        elif matrix[7] == nextNum:
            return 1, 7
        elif matrix[8] == nextNum:
            return pow(2, 0.5), 8
        
    elif currPos == 5:
        if matrix[0] == nextNum:
            return pow(5, 0.5), 0
        if matrix[1] == nextNum:
            return pow(2, 0.5), 1
        if matrix[2] == nextNum:
            return 1, 2
        if matrix[3] == nextNum:
            return 2, 3
        if matrix[4] == nextNum:
            return 1, 4
        if matrix[6] == nextNum:
            return pow(5, 0.5), 6
        if matrix[7] == nextNum:
            return pow(2, 0.5), 7
        if matrix[8] == nextNum:
            return 1, 8
        
    elif currPos == 6:
        if matrix[0] == nextNum:
            return 2, 0
        if matrix[1] == nextNum:
            return pow(5, 0.5), 1
        if matrix[2] == nextNum:
            return pow(8, 0.5), 2
        if matrix[3] == nextNum:
            return 1, 3
        if matrix[4] == nextNum:
            return pow(2, 0.5), 4
        if matrix[5] == nextNum:
            return pow(5, 0.5), 5
        if matrix[7] == nextNum:
            return 1, 7
        if matrix[8] == nextNum:
            return 2, 8
        
    elif currPos == 7:  
        if matrix[0] == nextNum:
            return pow(5, 0.5), 0
        if matrix[1] == nextNum:
            return 2, 1
        if matrix[2] == nextNum:
            return pow(5, 0.5), 2
        if matrix[3] == nextNum:
            return pow(2, 0.5), 3
        if matrix[4] == nextNum:
            return 1, 4
        if matrix[5] == nextNum:
            return pow(2, 0.5), 5
        if matrix[6] == nextNum:
            return 1, 6
        if matrix[8] == nextNum:
            return 1, 8
        
    elif currPos == 8:
        if matrix[0] == nextNum:
            return pow(8, 0.5), 0
        if matrix[1] == nextNum:
            return pow(5, 0.5), 1
        if matrix[2] == nextNum:
            return 2, 2
        if matrix[3] == nextNum:
            return pow(5, 0.5), 3 
        if matrix[4] == nextNum:
            return pow(2, 0.5), 4
        if matrix[5] == nextNum:
            return 1, 5
        if matrix[6] == nextNum:
            return 2, 6
        if matrix[7] == nextNum:
            return 1, 7
        if matrix[8] == nextNum:
            return pow(2, 0.5), 8



def main():
    #print("Lol")
    x = str(input())
    y = str(input())
    z = str(input())
    i = 0
    matrix = [int(i) for i in x.split()] + [int(i) for i in y.split()] + [int(i) for i in z.split()]
    length = 0
    #print(matrix)
    
    currPos = matrix.index(1)
    currentNum = 1
    while currentNum < 9:
        newLength, currPos = findNextAndCalcLength(currentNum, matrix, currPos)
        length = length + newLength
        currentNum = currentNum + 1
    #print(length)
        
    return 0

main()