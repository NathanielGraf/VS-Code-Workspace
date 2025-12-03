#Question 1:

import random
import math

#Generate a random number between 0 and 1 that will be our probability of heads 
p_heads = random.uniform(0, 1)
def biased_toss(p_heads):
    rand = random.uniform(0, 1)
    if rand < p_heads:
        return "H"
    else:
        return "T"
    
'''
We know that p(H, T) = p(T, H) for any p_heads
So we can toss until we get one of these, and 
can say if H comes first, return 1, else return 0.
'''

#Test for method to generate fair toss from biased_toss
def toss_until_first():
    while True:
        result1 = biased_toss(p_heads)
        result2 = biased_toss(p_heads)
        if result1 == "H" and result2 == "T":
            return 1
        elif result1 == "T" and result2 == "H":
            return 0
        else:
            continue
count = 0
for i in range(1000):
    count += toss_until_first()
print("Tested probability of heads: (should be close to 0.5)")
print(count / 1000)


#Question 2:

def pickIndex(w):
    total = sum(w)
    
    #If the weights pass this threshold, return that index
    threshold = random.uniform(0, total)
    
    #Subtract from threshold each time we go through a weight that doesn't surpass it
    for i, weight in enumerate(w):
        if threshold < weight:
            return i
        threshold -= weight
        
    #Nothing passed, so the last index is returned
    return len(w) - 1

#Test for pickIndex
weights = [1, 3, 2]
results = [0, 0, 0]
for _ in range(6000):
    results[pickIndex(weights)] += 1

print(f"Results: {results}, should be approximately [1000, 3000, 2000]")

#Question 3:

def returnKSamples(stream, k):
    reservoir = []
    
    #Loop through all numbers in stream
    for i, number in enumerate(stream):
        
        #Add all numbers to the reservoir until it is filled
        if i < k:
            reservoir.append(number)
            
        #Then, for each new number, randomly replace an existing number with prob k/(i+1)
        else:
            j = random.randint(0, i)
            if j < k:
                reservoir[j] = number
                
    return reservoir

# Test returnKSamples
stream = range(100)
sample = returnKSamples(stream, 5)
print(f"Sample: {sample}, should be 5 random items from 0-99")


#Question 4:

#Method to multiply matrices without numpy
def matrix_multiply(A, B):
    result = [[0.0 for z in range(4)] for z in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                result[i][j] += A[i][k] * B[k][j]
    return result

#Returns magnitude of vector
def get_magnitude(v):
    return math.sqrt(sum(x*x for x in v))

#QR decomposition algorithm (I had to look up how to do this with Gram-Schmidt process, it should converge to the correct eigenvalues)
def qr_decomposition(A):
    Q = [[0.0 for z in range(4)] for z in range(4)]
    R = [[0.0 for z in range(4)] for z in range(4)]
    
    #Get columns
    a_cols = [[A[i][j] for i in range(4)] for j in range(4)]
    
    for j in range(4):
        v = a_cols[j][:]
        
        #Orthogonalize against previous vectors
        for i in range(j):
            R[i][j] = sum(Q[k][i] * a_cols[j][k] for k in range(4))
            for k in range(4):
                v[k] -= R[i][j] * Q[k][i]
        
        #Normalize
        R[j][j] = get_magnitude(v)
        if abs(R[j][j]) > 1e-10:
            for i in range(4):
                Q[i][j] = v[i] / R[j][j]
        else:
            Q[j][j] = 1.0
    
    return Q, R

def getEigenvalues(matrix):
    
    #QR algorithm iterations
    A = [[matrix[i][j] for j in range(4)] for i in range(4)]

    #10000 runs should be good to converge along the diagonal
    for z in range(10000): 
        Q, R = qr_decomposition(A)
        A = matrix_multiply(R, Q)
    
    #Get eigenvalues
    eigenvalues = [A[i][i] for i in range(4)]
    
    #Return highest to lowest 
    return sorted(eigenvalues, reverse=True)

#Test cases:
test1 = [
    [5, 0, 0, 0],
    [0, 3, 0, 0],
    [0, 0, 2, 0],
    [0, 0, 0, 1]
]
print(f"Result: {getEigenvalues(test1)}, should be [5, 3, 2, 1]")

test2 = [
    [4, 1, 0, 0],
    [1, 3, 1, 0],
    [0, 1, 2, 1],
    [0, 0, 1, 1]
]
print(f"Result: {getEigenvalues(test2)}, should be approx [4.74, 3.17, 1.82, .25]")


#Question 5:

#Use Gauss Jordan elimination to find inverse
def matrixInverse(matrix):

    #Create augmented matrix by putting identity matrix to the right of input matrix
    n = 4
    augmented = []
    
    #For each row, copy the matrix, add n 0s, and then put the 0 on the diagonal distance
    for i in range(n):
        row = matrix[i][:] + [0.0] * n 
        row[n + i] = 1.0 
        augmented.append(row)
    
    #Make left matrix upper triangular, 1s on diagonal, 0s below
    for i in range(n):

        #Normalize current row so diagonal element becomes 1
        diagonal_value = augmented[i][i] 
        for j in range(2 * n): 
            augmented[i][j] /= diagonal_value
        
        #Eliminate all elements below current diagonal 
        for k in range(i + 1, n):

            factor = augmented[k][i]
        
            #Subtract factor * current_row from row k, this makes element in column i become zero
            for j in range(2 * n):
                augmented[k][j] -= factor * augmented[i][j]
    
    #Back sub to eliminate elements above diagonal
    #Start from last row and go up to first row 
    for i in range(n - 1, -1, -1): 
        for k in range(i - 1, -1, -1):
        
            #Do same eliminiation as before
            factor = augmented[k][i]
            for j in range(2 * n):
                augmented[k][j] -= factor * augmented[i][j]
    
    #Extract inverse, it is the right side of aug
    inverse = []
    for i in range(n):
        inverse.append(augmented[i][n:])
    
    return inverse

#Inverse test cases 
test_matrix = [
    [2, 0, 0, 0],
    [0, 3, 0, 0],
    [0, 0, 4, 0],
    [0, 0, 0, 5]
]
inv = matrixInverse(test_matrix)
print(f"Should be [0.5, 0.33, 0.25, 0.2] on diagonal")
for row in inv:
    print([x for x in row])

test_matrix2 = [
    [1, 2, 0, 0],
    [0, 1, 3, 0],
    [0, 0, 1, 4],
    [0, 0, 0, 1]
]
inv2 = matrixInverse(test_matrix2)
print(f"Should be [[1, -2, 6, -24], [0, 1, -3, 12], [0, 0, 1, -4], [0, 0, 0, 1]]")
for row in inv2:
    print([x for x in row])

#Question 6: 

#Transpose method - swaps rows and columns
def transpose(matrix):
    return [[matrix[j][i] for j in range(4)] for i in range(4)]


#Get's eigenvalues and eigenvectors of matrix via Jacobi method (I had to look up how to do this)
def jacobi_eigenvalue(matrix, max_iter=10000):
   
    n = 4
    #A is initial matrix
    A = [[matrix[i][j] for j in range(n)] for i in range(n)]
    
    #V begins as identity and will become eigenvectors 
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    
    #Iterate until matrix is diagonalized
    for iter in range(max_iter):
        
        #Find the largest non-diagonal element to eliminate
        max_val = 0
        p, q = 0, 1
        for i in range(n):
            for j in range(i + 1, n):
                if abs(A[i][j]) > max_val:
                    max_val = abs(A[i][j])
                    p, q = i, j
        
        #If the largest element is small enough, we have converged and are done
        if max_val < 1e-10:
            break
        
        #Get rotation angle to zero out A[p][q]
        if abs(A[p][p] - A[q][q]) < 1e-10:
            theta = math.pi / 4
        else:
            theta = 0.5 * math.atan(2 * A[p][q] / (A[p][p] - A[q][q]))
        
        c = math.cos(theta)
        s = math.sin(theta)
        
        
        #Store old values
        App = A[p][p]
        Aqq = A[q][q]
        Apq = A[p][q]
        
        #Add new diagonal elements
        A[p][p] = c * c * App - 2 * s * c * Apq + s * s * Aqq
        A[q][q] = s * s * App + 2 * s * c * Apq + c * c * Aqq
        
        #Set off diagonal to 0 
        A[p][q] = 0
        A[q][p] = 0
        
        #Apply the rotation to matrix A
        for i in range(n):
            if i != p and i != q:
                Aip = A[i][p]
                Aiq = A[i][q]
                A[i][p] = c * Aip - s * Aiq
                A[p][i] = A[i][p]
                A[i][q] = s * Aip + c * Aiq
                A[q][i] = A[i][q]
        
        #Update eigenvector matrix V
        for i in range(n):
            Vip = V[i][p]
            Viq = V[i][q]
            V[i][p] = c * Vip - s * Viq
            V[i][q] = s * Vip + c * Viq
    
    #After convergence, diagonal elements are eigenvalues
    eigenvalues = [A[i][i] for i in range(n)]
    
    #V contains eigenvectors as columns
    return eigenvalues, V

#Finds SVD of a 4x4 matrix
def SVD(matrix):
   
    n = 4
    
    #Compute A^T * A to get a symmetric matrix for jacobi 
    A_T = transpose(matrix)
    ATA = matrix_multiply(A_T, matrix)
    
    #Run jacobi to get eigenvalues and eigenvectors of ATA
    eigenvalues, V = jacobi_eigenvalue(ATA)
    
    
    #Get eigenvalues in sorted order and move eigenvectors accordingly
    eigen_pairs = [(eigenvalues[i], i) for i in range(n)]
    eigen_pairs.sort(reverse=True, key=lambda x: x[0])
    V_sorted = [[0.0 for _ in range(n)] for _ in range(n)]
    sigma_values = []
    
    for i, (eigen_val, orig_idx) in enumerate(eigen_pairs):
        for row in range(n):
            V_sorted[row][i] = V[row][orig_idx]
        
        #Use sqrt of eigenvalue as singular value
        sigma_values.append(math.sqrt(max(0, eigen_val)))
    
    #Create sigma, diagonal matrix with singular values on diagonal
    Sigma = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        Sigma[i][i] = sigma_values[i]
    
    #Compute U using U = A * V * Σ^-1
    AV = matrix_multiply(matrix, V_sorted)
    
    U = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if sigma_values[j] > 1e-10: 
                U[i][j] = AV[i][j] / sigma_values[j]
            else:
                U[i][j] = 0.0 
    
    #Transpose V to get V^T
    V_T = transpose(V_sorted)
    
    return U, Sigma, V_T



#Test SVD
diag_matrix = [
    [4, 0, 0, 0],
    [0, 3, 0, 0],
    [0, 0, 2, 0],
    [0, 0, 0, 1]
]

print("\nOriginal Matrix:")
U1, Sigma1, VT1 = SVD(diag_matrix)
for row in diag_matrix:
    print([x for x in row])

#Reconstruct original matrix from SVD components:
reconstructed1 = matrix_multiply(matrix_multiply(U1, Sigma1), VT1)
print("\nReconstructed Matrix:")
for row in reconstructed1:
    print([round(x, 4) for x in row])
    
diag_matrix = [
    [2, 1, 0, 0],
    [0, 2, 1, 0],
    [0, 0, 2, 1],
    [0, 0, 0, 2]
]
print("\nOriginal Matrix:")
U1, Sigma1, VT1 = SVD(diag_matrix)
for row in diag_matrix:
    print([x for x in row])

#Reconstruct original matrix from SVD components:
reconstructed2 = matrix_multiply(matrix_multiply(U1, Sigma1), VT1)
print("\nReconstructed Matrix:")
for row in reconstructed2:
    print([round(x, 4) for x in row])
