'''
You now work for a video game company - every programmer's dream! You are working on a multiplayer game where players cooperate to enter a maze and try to consume all of the “dots” as quickly as possible. Each player enters the maze at a different entrance. The mazes are randomly generated, so the minimum number of players needed to consume all of the dots can vary, and some dots may not be reachable at all.

You are working in the Quality Control department, analyzing the randomly generated mazes. For analysis, the mazes are represented in text. An X is a wall that cannot be crossed. Letters A-W are entrances. Players can only move up, down, left and right. Players can move though spaces and dots; moving over a dot eats it. If two doors are adjacent, players cannot move from one to the other. For example:

All of the reachable dots can be reached from entrances A and C (or, equivalently, B and C). There are three dots that cannot be reached.

Calculate the minimum number of players necessary to eat all the reachable dots, and how many dots are not reachable because they are walled off.

XXXXXXXAXXXXXXXBXXXX
X.. ..X.X...... ...X
X.XXX...X.X.XXXXXX.X
X.X.XXXXX.X.X....X.X
X.X... ...X.X.XX.X.X
X.X.X.XXXXXXX.XX.X.X
X.X.X.X...X...X....X
X.X.X.XXXXXXX.XXXX.X
X...X.X X.. ..X..X.X
XXXXXXXDXXXXXXXXCXXX

Input: 
This first line of input contains two integers n and m, 3 <= n, m <= 100
where n is the number of rows in the maze representation, and m is the number of columns.


Each of the next n lines contains a string of length exactly m, consisting only of the capital letters A through X, space, or period. This is the maze. The borders of the maze (rows 1 and n, columns, 1 and m) are guaranteed to consist only of capital letters A through X. There are no entrances (A-W) in the middle of the maze.

Output a line with two space-separated integers, the first of which is the minimum number of entrances necessary to enter in order to eat all of the dots (which may be 0 if no dots are reachable), and the second of which is the number of dots which cannot be reached.

Sample input 1:
10 20
XXXXXXXAXXXXXXXBXXXX
X.. ..X.X...... ...X
X.XXX...X.X.XXXXXX.X
X.X.XXXXX.X.X....X.X
X.X... ...X.X.XX.X.X
X.X.X.XXXXXXX.XX.X.X
X.X.X.X...X...X....X
X.X.X.XXXXXXX.XXXX.X
X...X.X X.. ..X..X.X
XXXXXXXDXXXXXXXXCXXX

Sample output 1: 
2 3

Sample input 2:
3 5
XDRVX
X.X.X
XXXXX

Sample output 2:
2 0

Sample input 3:
3 5
NAQXX
X X.X
XXXXX

Sample output 3:
0 1
'''


def isReachable(dot, entrance, matrix, n, m):
    
    #Find entrance
    for i in range(n):
        for j in range(m):
            if matrix[i][j] == entrance:
                entrance = (i,j)
                break
    
    colored = [[ False for i in range(0,m) ] for j in range(0,n)]
    
    open = [entrance]

    while len(open) != 0:
        (x,y) = open.pop()
        if x == dot[0] and y == dot[1]:
            return True
        elif x == 0 and y >= 0 and y < m and matrix[x][y] != "X" and not colored[x][y]:
            colored[x][y] = True
            open.extend([(x+1,y)])
            
        elif x >= 0 and y == 0 and y < m and matrix[x][y] != "X" and not colored[x][y]:
            colored[x][y] = True
            open.extend([(x,y+1)])
        
        elif x == n-1 and y >= 0 and y < m and matrix[x][y] != "X" and not colored[x][y]:
            colored[x][y] = True
            open.extend([(x-1,y)])
            
        elif x >= 0 and y == m-1 and y < m and matrix[x][y] != "X" and not colored[x][y]:
            colored[x][y] = True
            open.extend([(x,y-1)])   
            
        elif x >= 0 and y >= 0 and x < n and y < m and matrix[x][y] != "X" and not colored[x][y]:
            colored[x][y] = True
            open.extend([(x-1,y), (x,y-1), (x+1,y), (x,y+1)])

    return False

    

    
    





def main():
    
    n, m = [int(i) for i in input().split()]

    matrix = []
    
    for i in range(n):
        matrix.append(input())

    #print(matrix)

    #Find all entrances
    entrances = []
    for i in range(n):
        for j in range(m):
            if matrix[i][j] != 'X' and matrix[i][j] != '.' and matrix[i][j] != " ":
                entrances.append(matrix[i][j])
    
    #print(entrances)
    
    #Find all dots
    dots = []
    for i in range(n):
        for j in range(m):
            if matrix[i][j] == '.':
                dots.append((i,j))
                
    #print(dots)
    
    #Find all reachable dots
    
    reachable = []
    for i in range(len(dots)):
        for j in range(len(entrances)):
            if isReachable(dots[i], entrances[j], matrix, n, m):
                reachable.append(dots[i])
                break
    
    #print(reachable)
    
    #Find all unreachable dots
    unreachable = []
    
    for i in range(len(dots)):
        if dots[i] not in reachable:
            unreachable.append(dots[i])
            
    #print(unreachable)
    

    #Find minimum number of entrances
    
    minEntrances = 0
    goodentrances = []
    for i in range(len(entrances)):
        for j in range(len(reachable)):
            if isReachable(reachable[j], entrances[i], matrix, n, m):
                goodentrances.append(entrances[i])
                break
            
    
    
    
    for i in range(len(goodentrances)):
        for j in range(len(goodentrances)):
            if isReachable(goodentrances[i], goodentrances[j], matrix, n, m) and i != j:
                goodentrances.pop(j)
                break
            
                
    print(goodentrances)
    
    print(len(goodentrances), len(unreachable))
    
    
    
        
    return 0

main()