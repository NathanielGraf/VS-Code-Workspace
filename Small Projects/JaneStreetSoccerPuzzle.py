import numpy as np

#Function to calculate the markov chain matrix to find the expected value of a random walk returning to origin for Jane Street July 2022 Puzzle.

#Markov Chain itself
soccerballmatrix = [[0, 1, 0, 0, 0, 0, 0], [0, 0, 2/3, 0, 0, 0, 1/3], [0, 1/3, 1/3, 1/3, 0, 0, 0], [0, 0, 1/3, 1/3, 1/3, 0, 0], [0, 0, 0, 2/3, 0, 1/3, 0], [0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0]]

#Convert to array
array = np.array(soccerballmatrix)

#Function to calculate the probability of a random walk returning to origin in n steps
def probabilityNSteps(n):
    
    #Creates copy of array that we can square repeatedly while keeping original array intact
    arraydupe = array
    
    #Essentially talkes the array to the nth power
    for x in range(1,n):
        squaredarray = np.matmul(arraydupe, array)
        arraydupe = squaredarray

    #Returns the array coord we need to determine the number of steps to return to origin
    return (np.array(arraydupe) [0,6])

#Function to find expected value
def expectedValue(stepsToCalculate):
    
    #Create list to store values for each step
    sumlist = []
    
    #Calculate the probability of returning to origin in each step times the number of steps up to the number of steps we want to calculate
    for x in range(2, stepsToCalculate+1):
        probOfStepTimesStep = probabilityNSteps(x) * x
        sumlist.append(probOfStepTimesStep)

    return sum(sumlist)

#Run the function
answer = (expectedValue(4000))
print(answer)