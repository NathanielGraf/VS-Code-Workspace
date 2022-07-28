from ast import Break, Continue
import string
from urllib.request import HTTPBasicAuthHandler

'''
To play the game, do g = GameStateManager(dim), where dim is the dimension of your board.
Then you can call g.makeMove() to make your moves. 
'''
'''
Need a class to maintain the board, remember which pieces are where. 
Need a class to maintain piece attributes
Need a function which will check for a winner 
Need a function which will allow you to pass a piece to your opponent 

'''
class Pieces:
    
    def __init__(self):
        self.pieceslist = [(color, hole, height, shape) for color in [0,1] for hole in [0,1] for height in [0,1] for shape in [0,1]]
    
    def getPieceCoord(x, y):
        return Board.matrix[x][y]
    #self.pieceslist = [(color, hole, height, shape) for color in [0,1] for hole in [0,1] for height in [0,1] for shape in [0,1]]

class Board: 
    
    #Initialize Board 
    def __init__(self):
        
        #Adds dim to our function vars

        
        #Creates a row consisting of dim boxes, unformatted
        self.matrix = [" "] * 4
        
        self.clonematrix = [" "] * 4
        
        #Remakes the row dim times to make it 2d
        for x in range(0, 4): 
            self.matrix[x] = [" "]*4
            
        for x in range(0, 4):
            self.clonematrix[x] = [" "] * 4
    
    #Makes it so that you don't have to call Board each time you need to use row
    @staticmethod
    
    #Defines a rowMaker function to add in the dividers and newline into a given row
    def rowMaker(row): 
        return " " + " | ".join(row) + " " + "\n"

    #Converts the thing to a string
    def __str__(self): 
        
        #Defines the thing I will output so we can add my prints to it later
        str_output = ""
        
        '''
        Piece is in row in matrix
        Turn piece into string, then you can join the rows
        '''
        
        #Creates a range of size dim, which passes a row i into our rowMaker function
        for i in range(0, 4):
            for x in range(0,4):
                self.clonematrix[i][x] = "".join(str(x) for x in self.matrix[i][x])
            #Defines 1 row after it is passed through the rowMaker
            row = Board.rowMaker(self.clonematrix[i])
                                 
            #Creates horizontal lines that fit according to the dim, and then puts it after each row is created except for the last one
            horilines = "---" + "----" * (int(4) -1)
            str_output+=row
            if i < 4 - 1: 
                str_output+=horilines+'\n'
                
        #Return the finished board
        return str_output

    #Play function
    def play(self, piecetoplace, coordrow, coordcolumn): 
        
        """
        Coordrow gives row position
        Coordcolumn gives column position
        Can't take non-ints
        Token is X or O 
        Can't place a token in occupied square 
        Coord numbers must be less than dim
        """
        
        #Checks to make sure the token is X or O
        #if token != "X" and token != "O":
           # print("Please re-call the function, capital X or O only!")
          #  return None
        
        #Defines my row positions and column positions from the arguments
        rowpos = coordrow
        colpos = coordcolumn
    
        #Checked if the place we are placing the token is empty or not, if it isn't, give message
        if self.matrix[rowpos][colpos] != " ": 
            print("Please only place your token in an unoccupied square!")
            return None
        
        #Sets the position equal to the token
        self.matrix[rowpos][colpos] = piecetoplace
        
        #piececlass.pieceslist.remove(piecetoplace)
        
        #Call winner function to check for a winner
        Board.winner(self)
           
    #Winner function
    def winner(self):   
        
        #Set iterator i to 0
        i = 0
        
        #Makes x test through all rows
        for x in range(0, 4):
            
            #Loops z through all attributes
            for z in range(0, 4):
            
                #Makes i test through dim - 1, since we only need to compare twice
                while i < 3:
                
                #Compare row x column i to the one to the right of it, if it is the same, continue, if both comparisons are true, prints winner
                    
                    if self.matrix[x][i] != " " and self.matrix[x][i+1] != " ":
                        if ((self.matrix[x][i])[z] == (self.matrix[x][i+1])[z]):
                            if i + 2 == 4:
                                print("Player" + GameStateManager.getPlayerTurn() + " is the winner!")
                                return True
                            i = i + 1
                        
                        else: 
                            break
                    else:
                        break
            
            
        #Reset i to 0
        i = 0
        
        #Makes x test through all rows
        for x in range(0, 4):
            
            #Loops z through all attributes
            for z in range(0, 4):
            
                #Makes i test through dim - 1, since we only need to compare twice
                while i < 3:
                
                    if self.matrix[x][i] != " " and self.matrix[x+1][i] != " ":
                #Compare row x column i to the one to the right of it, if it is the same, continue, if both comparisons are true, prints winner
                        if ((self.matrix[x][i])[z] == (self.matrix[x+1][i])[z]):
                            if i + 2 == 4:
                                print("Player" + GameStateManager.getPlayerTurn() + " is the winner!")
                                return True
                            i = i + 1
                        
                        else: 
                            break
                    else:
                        break
        #Basically like the above functions, but with no rows/columns, and what i did above becomes x
        for x in range(0, 3):
            for z in range(0, 4):
                if self.matrix[x][i] != " " and self.matrix[x+1][i+1] != " ":
                    if ((self.matrix[x][i])[z] == (self.matrix[x+1][i+1])[z]):
                        if x + 2 == 4:
                            print("Player" + GameStateManager.getPlayerTurn() + " is the winner!")
                            return True   
                        i = i + 1
                    else: 
                        break
                else:
                    break
        #Reset i to 0
        i = 0
        
         #Basically like the above functions, but with no rows/columns, and what i did above becomes x
        for x in range(0, 3):
            for z in range(0, 4):
                if self.matrix[3-x][i] != " " and self.matrix[2-x][i+1] != " ":
                    if ((self.matrix[3-x][i])[z] == (self.matrix[2-x][i+1])[z]):
                        if x + 2 == 4:
                            print("Player" + GameStateManager.getPlayerTurn() + " is the winner!")
                            return True   
                    else: 
                        break
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
    def __init__(self): 
        
        #Define b as a board of size dim
        #self.b = Board()
        
        #Set turncount to 0
        self.turncount = 0
        
        #self.piecetoplace = self.getPieceToGive()
        
    #Define getToken function
    def getPieceToGive(self):
        
        piece = []
        #1 = square, 1 = hole, 1 = tall, 1 = black
        print("Please choose the attributes of the piece you would like to give to your opponent!")
        self.color = input("0 for white, 1 for black: ")
        self.hole = input("0 for no hole, 1 for hole: ")
        self.height = input("0 for short, 1 for tall: ")
        self.shape = input("0 for circle, 1 for square: ")
        piece.append(self.color)
        piece.append(self.hole)
        piece.append(self.height)
        piece.append(self.shape)
        
        if piece not in piececlass.pieceslist:
            print("That piece cannot be played!")
        
        
        
        #if piece not in piececlass.pieceslist:
            #print("Piece has already been used! Try again!")
            
        
        return piece
        
            
    #Define makeMove function
    def makeMove(self):
        
            
        piecetoplace = self.getPieceToGive()
            
        self.turncount = self.turncount + 1 
        
        #Takes my row coordinate as a user input
        coordrow = int(input(("Please type the row where you would like to place your token: ")))
        
        #Takes my column coordinate as a user input
        coordcolumn = int(input(("Please type the column where you would like to place your token: ")))
        
        #Gets the current token from the getToken function
        
        #Passes in these 3 arguments into the play function
        self.b.play(piecetoplace, coordrow, coordcolumn)
        
        if self.turncount == 16:
            print("It's a tie game!")
            return None
        
        
        
        #Print out b so the player can see the board 
        print(self.b)
        
    def getPlayerTurn(self):
        
        if self.turncount % 2 == 0: 
            return 2
        else:
            return 1
GameStateManager.b = Board()
piececlass = Pieces()
game = GameStateManager()
game.makeMove()