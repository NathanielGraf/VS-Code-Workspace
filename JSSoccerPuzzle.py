from ast import Break, Continue
import string
import numpy
from urllib.request import HTTPBasicAuthHandler

'''
To play the game, do g = GameStateManager(dim), where dim is the dimension of your board.
Then you can call g.makeMove() to make your moves. 
'''

class Board: 
    
    #Initialize Board 
    def __init__(self, dim):
        
        #Adds dim to our function vars
        self.dim = dim
        
        #Creates a row consisting of dim boxes, unformatted
        self.matrix = [" "] * dim
        
        #Remakes the row dim times to make it 2d
        for x in range(0, dim): 
            self.matrix[x] = [" "]*self.dim
    
    #Makes it so that you don't have to call Board each time you need to use row
    @staticmethod
    
    #Defines a rowMaker function to add in the dividers and newline into a given row
    def rowMaker(row): 
        return " " + " | ".join(row) + " " + "\n"

    #Converts the thing to a string
    def __str__(self): 
        
        #Defines the thing I will output so we can add my prints to it later
        str_output = ""
        
        #Creates a range of size dim, which passes a row i into our rowMaker function
        for i in range(0, self.dim):
            
            #Defines 1 row after it is passed through the rowMaker
            row = Board.rowMaker(self.matrix[i])
                                 
            #Creates horizontal lines that fit according to the dim, and then puts it after each row is created except for the last one
            horilines = "---" + "----" * (int(self.dim) -1)
            str_output+=row
            if i < self.dim - 1: 
                str_output+=horilines+'\n'
                
        #Return the finished board
        return str_output

    #Play function
    def play(self, token, coordrow, coordcolumn): 
        
        """
        Coordrow gives row position
        Coordcolumn gives column position
        Can't take non-ints
        Token is X or O 
        Can't place a token in occupied square 
        Coord numbers must be less than dim
        """
        
        #Checks to make sure the token is X or O
        if token != "X" and token != "O":
            print("Please re-call the function, capital X or O only!")
            return None
        
        #Defines my row positions and column positions from the arguments
        rowpos = coordrow
        colpos = coordcolumn
    
        #Checked if the place we are placing the token is empty or not, if it isn't, give message
        if self.matrix[rowpos][colpos] != " ": 
            print("Please only place your token in an unoccupied square!")
            return None
        
        #Sets the position equal to the token
        self.matrix[rowpos][colpos] = token
        
        #Call winner function to check for a winner
        Board.winner(self)
           
    #Winner function
    def winner(self):   
        
        #Set iterator i to 0
        i = 0
        
        #Makes x test through range dim
        for x in range(0, self.dim):
            
            #Makes i test through dim - 1, since we only need to compare twice
            while i < self.dim -1:
                
                #Compare row x column i to the one to the right of it, if it is the same, continue, if both comparisons are true, prints winner
                if (self.matrix[x][i] == "X" or self.matrix[x][i] == "O") and (self.matrix[x][i] == self.matrix[x][i+1]):
                    if i + 2 == self.dim:
                        print(self.matrix[x][0] + " is the winner!")
                        return True
                    i = i + 1
                    
                else: 
                    break
            
            
        #Reset i to 0
        i = 0
        
        #Test the above but columns
        for x in range(0, self.dim):
            
            
            while i < self.dim -1:
                if (self.matrix[i][x] == "X" or self.matrix[i][x] == "O") and (self.matrix[i][x] == self.matrix[i+1][x]):
                    if i + 2 == self.dim:
                        print(self.matrix[0][x] + " is the winner!")
                        return True
                    i = i + 1
                    
                else: 
                    break
            
        #Reset i to 0
        i = 0
        
        #Basically like the above functions, but with no rows/columns, and what i did above becomes x
        for x in range(0, self.dim - 1):
            if (self.matrix[x][x] == "X" or self.matrix[x][x] == "O") and (self.matrix[x][x] == self.matrix[x+1][x+1]):
                if x + 2 == self.dim:
                    print(self.matrix[x][x] + " is the winner!")
                    return True   
            else: 
                break
    
        #Reset i to 0
        i = 0
        
        #Same as above but other diagonal
        for x in range(0, self.dim - 1):
            if (self.matrix[self.dim -1 - x][x] == "X" or self.matrix[self.dim -1 - x][x] == "O") and (self.matrix[self.dim -1 - x][x] == self.matrix[self.dim -2 -x][x+1]):
                if x + 2 == self.dim:
                    print(self.matrix[self.dim -1 -x][x] + " is the winner!")
                    return True   
            else: 
                break
            
#GameStateManager Class
class GameStateManager: 
    '''
    Needs to:
    See which tokens turn it is.
    Take inputs from the players.
    Call the play function to place tokens. 
    Call the winner function to check the winner.
    '''
    #Initialize the class
    def __init__(self, dim): 
        
        #Define b as a board of size dim
        self.b = Board(dim)
        
        #Set lastmove for my getToken() function
        self.lastmove = "O"
        
        #Set turncount to 0
        self.turncount = 0
    
    #Define getToken function
    def getToken(self): 
        
        #Increment turncount
        self.turncount = self.turncount + 1

        #Give the opposite of the lastmove as the new current token
        if self.lastmove == "X":
            self.lastmove = "O"
            return("O")
        else:
            self.lastmove = "X"
            return("X")
            
    #Define makeMove function
    def makeMove(self):
        
        #Check for a tie if makeMove is rerun after a full board, ends the game. 
        if self.turncount >= 10: 
            print("Tie game!")
        
        else:
            #Takes my row coordinate as a user input
            coordrow = int(input(("Please type the row where you would like to place your token: ")))
            
            #Takes my column coordinate as a user input
            coordcolumn = int(input(("Please type the column where you would like to place your token: ")))
            
            #Gets the current token from the getToken function
            token = self.getToken()
            
            #Passes in these 3 arguments into the play function
            self.b.play(token, coordrow, coordcolumn)
            
            #Print out b so the player can see the board 
            print(self.b)
            
