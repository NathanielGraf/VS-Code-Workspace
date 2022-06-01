class TicTacToe
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.currentwinner = None
        
    def printboard(self):
        for row in [self.board[i*3:(i+1)*3] for i in range (3)]:
            print('| ' + ' | '.join(row) + ' |')
            
    @staticmethod
    def printboardnums():
        numberboard = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in numberboard:
            print('| ' + ' | '.join(row) + ' |')
            
    def availablemoves(self):
        moves = []
        for (i, spot) in enumerate(self.board):
            if spot == ' ': 
                moves. =