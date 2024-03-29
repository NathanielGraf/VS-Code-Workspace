from ast import Break, Continue
import string
from urllib.request import HTTPBasicAuthHandler
import random
import copy

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
        self.pieceslist = [[str(color), str(hole), str(height), str(shape)] for color in [0,1] for hole in [0,1] for height in [0,1] for shape in [0,1]]
        self.coordinates = [[x,y] for x in range(0,4) for y in range(0,4)]

    def getPieceCoord(x, y):
        return Board.matrix[x][y]
    #self.pieceslist = [(color, hole, height, shape) for color in [0,1] for hole in [0,1] for height in [0,1] for shape in [0,1]]

class Board: 
    
    #Initialize Board 
    def __init__(self):
        
        #Creates a row consisting of dim boxes, unformatted
        self.matrix = [" "] * 4
        
        #Creates a clone of the matrix, so we can modify it without affecting the original
        self.clonematrix = [" "] * 4
        
        self.checkmatrix = [" "] * 4
        
        #Remakes the row 4 times to make it 2d
        for x in range(0, 4): 
            self.matrix[x] = [" "]*4
        
        #Remakes the clone 4 times to make it 2d
        for x in range(0, 4):
            self.clonematrix[x] = [" "] * 4
            
        for x in range(0, 4):
            self.checkmatrix[x] = [" "] * 4
    
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
    def play(self, piecetoplace, coordrow, coordcolumn, board): 
        
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
        if board[rowpos][colpos] != " ": 
            raise Exception("Please only place your token in an unoccupied square!")
        
        #Sets the position equal to the token
        board[rowpos][colpos] = piecetoplace
        
        #piececlass.pieceslist.remove(piecetoplace)
        
       
           
    #Winner function
    def winner(self, board):   
        
        
        
        #Set iterator i to 0
        i = 0
        
        #Makes x test through all rows
        for x in range(0, 4):
            
            #Loops z through all attributes
            for z in range(0, 4):
            
                #Makes i test through dim - 1, since we only need to compare twice
                for i in range(0, 3):
                
                #Compare row x column i to the one to the right of it, if it is the same, continue, if both comparisons are true, prints winner
                    
                    if board[x][i] != " " and board[x][i+1] != " ":
                        if ((board[x][i])[z] == (board[x][i+1])[z]):
                            if i + 2 == 4:
                                #Print("Player " + game.getPlayerTurn() + " is the winner!")
                                return True
                                
                            
                        
                        else: 
                            
                            break
                    else:
                        
                        break
            
            
        #Set iterator i to 0
        i = 0
        #Makes x test through all rows
        for x in range(0, 4):
            #Loops z through all attributes
            for z in range(0, 4):
                #Makes i test through dim - 1, since we only need to compare twice
                for i in range(0, 3):
                #Compare row x column i to the one to the right of it, if it is the same, continue, if both comparisons are true, prints winner
                    if board[i][x] != " " and board[i+1][x] != " ":
                        if ((board[i][x])[z] == (board[i+1][x])[z]):
                            if i + 2 == 4:
                                #print("Player " + game.getPlayerTurn() + " is the winner!")
                                return True
                            
                        
                        else: 
                            break
                    else:
                        break
            
        #Basically like the above functions, but with no rows/columns, and what i did above becomes x
        #for x in range(0, 3):
            
        for z in range(0, 4):
            for i in range(0, 3):
                if board[i][i] != " " and board[i+1][i+1] != " ":
                    if ((board[i][i])[z] == (board[i+1][i+1])[z]):
                    
                        if i + 2 == 4:
                            #print("Player " + game.getPlayerTurn() + " is the winner!")
                            return True   
                        
                    else: 
                        break
                else:
                    break
        #Reset i to 0
        i = 0
        #0001 0010 1010 1111
         #Basically like the above functions, but with no rows/columns, and what i did above becomes x
        #for x in range(0, 3):
        for z in range(0, 4):
            for i in range(0, 3):
                if board[3-i][i] != " " and board[2-i][i+1] != " ":
                    if ((board[3-i][i])[z] == (board[2-i][i+1])[z]):
                        if i + 2 == 4:
                            #print("Player " + game.getPlayerTurn() + " is the winner!")
                            return True  
                
                    else: 
                        break
                else:
                    break
                
        if len(piececlass.coordinates) == 0:
            print("It's a tie game!")
            return True
                    
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
        self.board = Board()
        
        #Set turncount to 0
        self.turncount = 0
        
        #self.piecetoplace = self.getPieceToGive()
        
        print("Player 2:")
        
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
        
        #Checks if the piece is valid
        if piece not in piececlass.pieceslist:
            raise Exception("Piece not in list!")
        else:
            #Removes my piece from the list of pieces so it cannot be used again
            piececlass.pieceslist.remove(piece)        
        
        #Returns the piece we want to use next time
        return piece
    
    def getPieceToGiveRandom(self):
        #Gets a random piece from the list of pieces
        piece = random.choice(piececlass.pieceslist)
        #Removes the piece from the list of pieces so it cannot be used again
        piececlass.pieceslist.remove(piece)
        #Returns the piece we want to use next time
        return piece
        
    '''
    Need GameStateManager to have a run function, while board.winner != true, makeMove or whatever
    Also add player pick and move ordering
    
    
    '''
    def makeMoveRandom(self):
        piecetoplace = self.getPieceToGiveRandom()
        
        self.turncount = self.turncount + 1
        
        print("Turn " + str(self.turncount))
        
        print("Player " + game.getPlayerTurn() + "'s turn!")
        
        coord = random.choice(piececlass.coordinates)
        
        coordrow = coord[0]
        coordcolumn = coord[1]
        
    
        piececlass.coordinates.remove(coord)
        
        self.board.play(piecetoplace, coordrow, coordcolumn, self.board.matrix)
        
        print(self.board)
        
        #if self.turncount == 16:
            #print("It's a tie game!")
            #return True
        
        '''
        CHANGE b to board 
        Also change Board.matrix to board.matrix
        '''
            
    def makeMoveAlwaysWin(self):
        piecetoplace = self.getPieceToGiveRandom()
        
        self.turncount = self.turncount + 1
        
        print("Turn " + str(self.turncount))
        
        print("Player " + game.getPlayerTurn() + "'s turn!")
        
        
        if self.alwaysWinIfPossibleCheck(piecetoplace) == False:
            coord = random.choice(piececlass.coordinates)
        else:
            coord = self.alwaysWinIfPossibleCheck(piecetoplace)
        
        coordrow = coord[0]
        coordcolumn = coord[1]
        
    
        piececlass.coordinates.remove(coord)
        
        self.board.play(piecetoplace, coordrow, coordcolumn, self.board.matrix)
        
        print(self.board)
        
        #if self.turncount == 16:
            #print("It's a tie game!")
            #return True
        
        '''
        CHANGE b to board 
        Also change Board.matrix to board.matrix
        '''
            
    
    #Define makeMove function
    def makeMove(self):
        #Regression testing, save as a test case.
        
        
            
        piecetoplace = self.getPieceToGive()
        
        self.turncount = self.turncount + 1 
        
        print("Turn " + str(self.turncount))
        
        print("Player " + game.getPlayerTurn() + "'s turn!")
        
        
        #Takes my row coordinate as a user input
        coordrow = int(input(("Please type the row where you would like to place your token: ")))
        
        #Takes my column coordinate as a user input
        coordcolumn = int(input(("Please type the column where you would like to place your token: ")))
        
        #Gets the current token from the getToken function
        
        #Passes in these 3 arguments into the play function
        self.board.play(piecetoplace, coordrow, coordcolumn, self.board.matrix)
        
        #if self.turncount == 16:
            #print("It's a tie game!")
            #return None
    
        
        
        #Print out b so the player can see the board 
        print(self.board)
        
    def getPlayerTurn(self):
        
        if self.turncount % 2 == 0: 
            return "2"
        else:
            return "1"
        
    def alwaysWinIfPossibleCheck(self, piecetoplace):
        self.piecetoplace = piecetoplace
        for i in range(0, len(piececlass.coordinates)):
            coord = piececlass.coordinates[i]
            coordrow = coord[0]
            coordcolumn = coord[1]
            
            self.board.checkmatrix = copy.deepcopy(self.board.matrix)
            
            self.board.play(piecetoplace, coordrow, coordcolumn, self.board.checkmatrix)
        
            if self.board.winner(self.board.checkmatrix) == True:
                return coord
            
        return False
            
            
            
            
            
          

piececlass = Pieces()
game = GameStateManager()
while game.board.winner(game.board.matrix) != True:
    game.makeMoveAlwaysWin()
if game.board.winner(game.board.matrix) == True:
    print("Player " + game.getPlayerTurn() + " is the winner!")

'''
ALWAYS WIN!:

If you are given a piece which has a winning spot, you must play it there:

Take the piece
Place it in every spot on a fake board
if it makes a win, play it there

'''