import math
import random

class Player:
    def __init__(self, letter):
        self.letter = letter 
        
    def getmove(self, game):
        pass

class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
        
    def getmove(self, game):
        pass
    
class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
        
    def getmove(self, game):
        pass