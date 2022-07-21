import numpy as np

soccerballmatrix = [[0, 1, 0, 0, 0, 0, 0], [0, 0, 2/3, 0, 0, 0, 1/3], [0, 1/3, 1/3, 1/3, 0, 0, 0], [0, 0, 1/3, 1/3, 1/3, 0, 0], [0, 0, 0, 1/3, 1/3, 1/3, 0], [0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
A = np.array(soccerballmatrix)
#print(A)

def probabilityNSteps(n):
    Y = A
    for x in range(1,n):
        probabilitynsteps = np.matmul(Y, A)
        #print(probabilitynsteps)
        Y = probabilitynsteps
    
    #print(np.array(Y) [0,0])
    return (np.array(Y) [0,6])
    #return int(probabilitynsteps)

def probabilitylessNSteps(n):
    sumlist = []
    for x in range(2, n+1):
        #print(probabilityNSteps(x))
        sumlist.append(probabilityNSteps(x))
        #print(sumlist)
    return sum(sumlist)
        

#Plane
 
answer = (probabilitylessNSteps(100))
print(answer)

soccerballmatrix = [[0, 1, 0, 0, 0, 0, 0], [0, 0, 2/3, 0, 0, 0, 1/3], [0, 1/3, 1/3, 1/3, 0, 0, 0], [0, 0, 1/3, 1/3, 1/3, 0, 0], [0, 0, 0, 1/3, 1/3, 1/3, 0], [0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
A = np.array(soccerballmatrix)
#print(A)

def probabilityNSteps(n):
    Y = A
    for x in range(1,n):
        probabilitynsteps = np.matmul(Y, A)
        #print(probabilitynsteps)
        Y = probabilitynsteps
    
    #print(np.array(Y) [0,0])
    return (np.array(Y) [0,6])
    #return int(probabilitynsteps)

def probabilitylessNSteps(n):
    sumlist = []
    for x in range(2, n+1):
        #print(probabilityNSteps(x))
        sumlist.append(probabilityNSteps(x))
        #print(sumlist)
    return sum(sumlist)
        


 
answer = (probabilitylessNSteps(100))
print(answer)